import docker

client = docker.from_env()
container = None

try:
    print("Starting container with AppArmor profile...")
    container = client.containers.run(
        "flask-apparmor",
        ports={"5000/tcp": 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
    )

    print(f"Container started: {container.short_id}")
    print("\n--- Testing Restricted Actions ---")

    for command in ["cat /etc/passwd", "/bin/bash"]:
        exit_code, output = container.exec_run(command)
        print(
            f"Command: {command}\n"
            f"Exit Code: {exit_code}\n"
            f"Output: {output.decode(errors='replace')}"
        )
finally:
    if container is not None:
        print("\nStopping the container...")
        container.stop()
        container.remove()
        print("Container stopped.")
