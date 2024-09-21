import rohub
import os
import zipfile
import pathlib
import sys
from dotenv import load_dotenv


def main():
    # get all inputs from the action
    rohub_user = (
        sys.argv[1] if len(sys.argv) > 1 else os.environ.get("INPUT_ROHUB-USER")
    )
    rohub_password = (
        sys.argv[2] if len(sys.argv) > 2 else os.environ.get("INPUT_ROHUB-PASSWORD")
    )

    # log into rohub
    try:
        print("Logging into rohub...")
        rohub.login(rohub_user, rohub_password)
    except Exception as e:
        print(f"::error::Failed to log into rohub: {e}")
        return

    rohub_id = None
    # check if there is a rocrate-metadata.ldjson file
    if pathlib.Path("rocrate-metadata.ldjson").exists():
        # get the rohub id
        rohub_id = get_rohub_id()
        print(f"Found rocrate-metadata.ldjson file. ROHub ID is {rohub_id}")

    if rohub_id is None:
        # get title of the gh repository
        repo_name = os.getenv("GITHUB_REPOSITORY")
        repo_name = repo_name.split("/")[-1]
        print(f"Repository name: {repo_name}")
        # create a new ROHub project
        pd = pathlib.Path(__file__).parent
        try:
            print("Creating a new ROHub project...")
            ro_object = rohub.ros_create(repo_name, ["earth sciences"])
            rohub_id = ro_object["identifier"]
            print(f"Created a new ROHub project with ID {rohub_id}")

            # create a zip file for the rocrate
            exclude_files = [".git", ".env", ".gitignore"]

            zipf = zipfile.ZipFile("demo_rohub.zip", "w", zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(pd):
                # Exclude directories listed in exclude_files
                dirs[:] = [d for d in dirs if d not in exclude_files]
                for file in files:
                    if file not in exclude_files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, pd)
                        zipf.write(file_path, arcname)
            zipf.close()

            # add the zip file to the ro project
            path_to_zip = pd / "demo_rohub.zip"
            rohub.ros_upload_resources(rohub_id, path_to_zip)

            # delete the zip file
            os.remove(path_to_zip)

        except Exception as e:
            print(f"::error::Failed to create a new ROHub project: {e}")
            return

    print(rohub_id)
    # get the rocrate metadata jsonld file
    try:
        rohub.ros_export_to_rocrate(
            rohub_id, "rocrate-metadata", pd, use_format="jsonld"
        )
    except Exception as e:
        print(f"::error::Failed to export to rocrate: {e}")
        return


def get_rohub_id():
    # get the rohub id from the rocrate-metadata.ldjson file
    with open("rocrate-metadata.ldjson", "r") as f:
        metadata = json.load(f)
    graph = metadata["@graph"]
    for item in graph:
        if item["@id"] == "./":
            return item["identifier"].split("/")[-1]


if __name__ == "__main__":
    main()
