# Backend
This is a quick instruction guide on how to setup the project for yourself.
This is an actionable guide, meaning you will copy-paste a couple of lines of code.
And your development environment will be ready to go!

### Environmenet variables

1. Copy the .env.example file -> .env
`$ cp .env.example .env`

2. Fill out all of the environment varialbes (Check out the links / resources for each of them!)

3. Activate the virtual environment
`$ source .venv/bin/activate`

4. Install the python packages
`$ pip install -r requirements.txt`

5. If this is your first time running the project locally, please run the bootstrap (Or on every new branch you make!)
`python3 bootstrap-backend.py`

**NOTE** This will require you to fill out a ton of information.
We are always trying to keep the code consise & attempting to make the setup as easy for new developers to the project as possible.
If you get stuck at any point. Just contact the contributors on discord `adoniscodes` or `williamferns`

### Setup Project + Requirements for Lambdas
This will quickly guide on how to setup the virtual environment for aws cdk lambdas.

1. Firstly cd into the python directory
`$ cd backend/python` 

2. Enable the virtual environment / create it
```bash
$ rm -rf venv
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

---

### SUPABASE: Development Settings / Help
You will be using Supabase. Meaning you need to know a bit about the ins-and-outs of the supabase cli to do migrations.
Here is a quick guide on how to export the migrations / import them & how to save them to a remote database:

`npx supabase db pull` will pull down the config from the table you linked environment variable ($SUPABASE_PROJECT_REF)

`npx supabase migration up` will take the local migration scripts, and then apply them locally.

`npx supabase db push` will take the local migration scripts, and push them up to the remote project ($SUPABASE_PROJECT_REF)

---

### AWS CDK: Developmenet Settings / Help
You will also interact a ton with the AWS toolchain. Mostly AWS CDK.
Here are a couple of commands & guides to get you quickly off the ground.

HOW TO SETUP AWS LAMBDAS: https://youtu.be/o3s4VqlMsT8?si=ttvhKfdIkQt1FdZ0
HOW TO INTEGRATE EXTERNAL DEPENDENCIES AWS LAMBDAS: https://www.youtube.com/watch?v=FnfnDc6TVjw

`cdk synth` Will build the changes for cdk locally, best to use to test if your code compiles
`cdk deploy` Pushes your changes up to remote aws account
`<command> --verbose` The verbose logs everything incase you run into errors

**NOTE** There will maybe be some errors. Here are some common solutions that worked for us.
1. Ensure your virtual environment is deleted in the `backend/python`
2. Run the commands as sudo
3. Attempt to modify the permissions of docker & then do the past 2 steps again:
```bash
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "/home/$USER/.docker" -R
```

---

### HELP / SUPPORT
We are always trying to keep the code consise & attempting to make the setup as easy for new developers to the project as possible.
If you get stuck at any point. Just contact the contributors on discord `adoniscodes` or `williamferns`
If you found a possible solution before getting into contact, feel free to modify the documentation, bootstrap scripts & more to accomodate these changes.
Thanks!
