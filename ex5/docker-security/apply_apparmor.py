import docker

client = docker.from_env()

print("Building image from Dockerfile...")
client.images.build(path=".", tag="flask-apparmor")

print("Running container with AppArmor profile...")
container = client.containers.run(
    "flask-apparmor",
    ports={"5000/tcp": 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True,
)

try:
    print(f"Container started: {container.short_id}")
    container_info = client.api.inspect_container(container.id)
    print(
        "AppArmor profile configured:",
        container_info["HostConfig"]["SecurityOpt"],
    )
finally:
    print("Stopping the container...")
    container.stop()
    container.remove()
    print("Container stopped.")
