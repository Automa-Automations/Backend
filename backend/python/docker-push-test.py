import docker

client = docker.from_env()

client.login(username='adoniscodes', password='<password here>')

for line in client.images.push('adoniscodes/lala', tag='latest', stream=True):
    print(line)
