import dataclasses 
import datetime
from typing import Optional, BinaryIO
import base64

@dataclasses.dataclass
class Profile:
    id: str = dataclasses.field(init=False)
    username: str
    updated_at: datetime.datetime
    full_name: str
    avatar_url: str
    website: str
    expiry_date: datetime.datetime
    stripe_customer_id: str

    def to_dict(self):
        return dataclasses.asdict(self)
    
@dataclasses.dataclass
class DatabaseSyncedProfile():
    def __init__(self, *args, **kwargs):
        self._id = kwargs.pop('id')
        self._updated_at = kwargs.pop('updated_at')
        self._full_name = kwargs.pop('full_name')
        self._avatar_url = kwargs.pop('avatar_url')
        self._website = kwargs.pop('website')
        self._expiry_date = kwargs.pop('expiry_date')
        self._stripe_customer_id = kwargs.pop('stripe_customer_id')
        super().__init__(*args, **kwargs)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        pass # read-only

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value):
        if not isinstance(value, datetime.datetime):
            return # We don't want to set it to an invalid value
        self._updated_at = value

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self._full_name = value

    @property
    def avatar_url(self):
        return self._avatar_url

    @avatar_url.setter
    def avatar_url(self, value):
        """Expects a File Object, Base64 String, or URL"""
        if not isinstance(value, str):
            return
        file_object: Optional[BinaryIO] = None
        if 'http' in value:
            # Attempt to download it
            # For now we will just download a random image
            image_url = "https://picsum.photos/200"
            import requests
            response = requests.get(image_url)
            response_bytes = response.content
            file_object = response_bytes
        elif 'data:image' in value:
            value = value.split(',')[1]
            file_object = base64.b64decode(value)
        elif isinstance(value, BinaryIO):
            file_object = value

        supabase_url = "TODO: Upload the file_object"
        self._avatar_url = supabase_url

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, value):
        # TODO: Validate the URL using AI reading + Score > 0.5 (Else Null)
        self._website = value

    @property
    def expiry_date(self):
        return self._expiry_date

    @expiry_date.setter
    def expiry_date(self, value):
        if not isinstance(value, datetime.datetime):
            return
        self._expiry_date = value
    
    @property
    def stripe_customer_id(self):
        return self._stripe_customer_id

    @stripe_customer_id.setter
    def stripe_customer_id(self, value):
        # TODO: Update all the references in the database
        # TODO: Update the Stripe Customer
        self._stripe_customer_id = value
    
    @staticmethod
    def from_dict(data: dict):
        return DatabaseSyncedProfile(**data)

    def to_dict(self):
        # Loop over all of the properties
        output_dict = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                key = key[1:]
            output_dict[key] = value
        return output_dict

