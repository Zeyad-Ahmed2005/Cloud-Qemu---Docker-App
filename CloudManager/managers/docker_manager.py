from utils.cmd_runner import run_command
import os


class DockerManager:
    def __init__(self):
        pass

    def list_images(self):
        """
        Lists local docker images.
        """
        # Format for easier parsing? --format "{{.Repository}}:{{.Tag}} {{.ID}}"
        # For display, standard output might be enough if we just dump it to a text box,
        # but for a "List View", we might want structure.
        # Let's return raw string for now for simplicity, or try to parse.
        return run_command("docker images")

    def search_hub(self, term):
        """
        Searches DockerHub for images.
        """
        return run_command(f"docker search {term}")

    def pull_image(self, image_name):
        """
        Pulls an image from DockerHub.
        """
        return run_command(f"docker pull {image_name}")

    def create_dockerfile(self, path, content):
        """
        Creates a Dockerfile at the specified path.
        """
        try:
            # Ensure filename is Dockerfile if directory is passed?
            # The requirements say "ask about the path to save the dockerfile".
            # Users might provide a directory or full path.
            if os.path.isdir(path):
                file_path = os.path.join(path, "Dockerfile")
            else:
                file_path = path

            with open(file_path, "w") as f:
                f.write(content)
            return True, f"Dockerfile saved to {file_path}"
        except Exception as e:
            return False, str(e)

    def build_image(self, dockerfile_path, tag):
        """
        Builds a docker image from a Dockerfile.
        """
        # docker build -t tag_name -f path/to/Dockerfile context_dir
        # Usually context dir is the folder containing the Dockerfile.

        if os.path.isfile(dockerfile_path):
            context_dir = os.path.dirname(dockerfile_path)
            # -f might be needed if name isn't Dockerfile or if we want to be explicit
            command = f'docker build -t {tag} -f "{dockerfile_path}" "{context_dir}"'
            return run_command(command)
        else:
            return False, "Invalid Dockerfile path"

    def list_containers(self):
        """
        Lists running containers.
        """
        return run_command("docker ps")

    def stop_container(self, container_id):
        """
        Stops a running container.
        """
        return run_command(f"docker stop {container_id}")
