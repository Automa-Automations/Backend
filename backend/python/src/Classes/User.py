import dataclasses 
import datetime
from typing import Any
from src.utils import update_value, upload_file, download_file_url, get_value
import base64

class CannotModifyUserIdException(Exception):
    """Raised when the programmer attempts to modify the UserID!"""
    pass

class NotValidFullNameException(Exception):
    """Raised when the programmer attempts to modify the UserID!"""
    pass

@dataclasses.dataclass
class Profile:
    id: str
    username: str
    updated_at: datetime.datetime
    full_name: str
    avatar_url: str
    website: str
    expiry_date: datetime.datetime
    stripe_customer_id: str
    plan_type: str = "free"
    credits: int = 0

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def from_dict(data: dict):
        return Profile(**data)

    @staticmethod
    def from_id(id: str):
        value = get_value(table='profiles', line=id.lower())
        return Profile.from_dict(value)

    @staticmethod
    def to_synced_profile(profile: 'Profile'):
        return DatabaseSyncedProfile.from_dict(profile.to_dict())


@dataclasses.dataclass
class DatabaseSyncedProfile():
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')
        self._updated_at = kwargs.pop('updated_at')
        self._full_name = kwargs.pop('full_name')
        self._avatar_url = kwargs.pop('avatar_url')
        self._website = kwargs.pop('website')
        self._expiry_date = kwargs.pop('expiry_date')
        self._stripe_customer_id = kwargs.pop('stripe_customer_id')
        self._plan_type = kwargs.pop('plan_type', "free")
        self._credits = kwargs.pop('credits', 0)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise CannotModifyUserIdException
        pass # read-only

    @property
    def updated_at(self):
        self._sync()
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value):
        if not isinstance(value, datetime.datetime):
            raise ValueError(f"Cannot have datatype of {type(value)} for value \"updated_at\" Expecting datetime.datetime")

        self._update('updated_at', value, updated_at=False)
        self._updated_at = value

    @property
    def full_name(self):
        self._sync()
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        if len(value.split(" ")) > 1 and isinstance(value, str):
            self._update('full_name', value)
            self._full_name = value
            return

        raise NotValidFullNameException

    @property
    def avatar_url(self):
        self._sync()
        return self._avatar_url

    @avatar_url.setter
    def avatar_url(self, value):
        """Expects a File Object, Base64 String, or URL. And must be in png format!"""
        if 'http' in value:
            # Attempt to download it
            # For now we will just download a random image
            file_object = download_file_url(from_=value)
        elif 'data:image' in value:
            value = value.split(',')[1]
            file_object = base64.b64decode(value)
        elif isinstance(value, bytes):
            file_object = value
        else:
            raise ValueError(f"User \"avatar_url\" expect http:// or https:// or base64 or bytes object, but recieved {value} of type {type(value)} instead!")

        supabase_url = upload_file(bucket_name='avatars', path_on_bucket=f"{self._id}.png", content=file_object)
        self._update('avatar_url', supabase_url)
        self._avatar_url = supabase_url

    @property
    def website(self):
        self._sync()
        return self._website

    @website.setter
    def website(self, value):
        # TODO: Validate the URL using AI reading + Score > 0.5 (Else Null)
        self._update('website', value)
        self._website = value

    @property
    def expiry_date(self):
        self._sync()
        return self._expiry_date

    @expiry_date.setter
    def expiry_date(self, value):
        print("Updating Expiry Date")
        self._update('expiry_date', value)
        self._expiry_date = value
            

    @property
    def stripe_customer_id(self):
        self._sync()
        return self._stripe_customer_id

    @stripe_customer_id.setter
    def stripe_customer_id(self, value):
        # TODO: Update all the references in the database
        # TODO: Update the Stripe Customer
        self._update('stripe_customer_id', value)
        self._stripe_customer_id = value

    @property
    def plan_type(self):
        self._sync()
        return self._plan_type
    
    @plan_type.setter
    def plan_type(self, value):
        plan = get_value(table='plans', line=value)
        if not plan:
            raise ValueError(f"Plan with ID {value} does not exist!")

        self._update('plan_type', value)
        self._plan_type = value
    
    @property
    def credits(self):
        self._sync()
        return self._credits
    
    @credits.setter
    def credits(self, value):
        self._update('credits', value)
        self._credits = value

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
    
    def _update(self, val: str, new_value: Any, updated_at: bool =True):
        updated_at_now = datetime.datetime.now()
        table = "profiles"
        line = self._id
        val = val
        line_name = 'id'

        update_value(table=table, line=line, val=val, new_value=new_value, line_name=line_name)
        if updated_at:
            update_value(table=table, line=line, val='updated_at', new_value=updated_at_now, line_name=line_name)
    
    def _sync(self):
        new_data = get_value(table='profiles', line=self._id)
        for key, value in new_data.items():
            if key.startswith('_'):
                key = key[1:]
            setattr(self, f'_{key}', value)

    @staticmethod
    def from_id(id: str):
        value = get_value(table='profiles', line=id.lower())
        return DatabaseSyncedProfile.from_dict(value)
