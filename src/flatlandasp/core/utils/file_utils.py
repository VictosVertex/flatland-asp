import json
import os


def create_path_if_not_exist(*, path: str) -> None:
    does_exist = os.path.exists(path=path)
    if not does_exist:
        os.makedirs(path)
        print(f"Path generated: {path}")


def write_lines_to_file_in_output(*, path: str, file_name: str, lines: list[str]) -> None:
    create_path_if_not_exist(path=path)

    with open(f'{path}/{file_name}', 'w') as f:
        f.writelines(line + '\n' for line in lines)


def get_file_names_in_path(*, path: str) -> list[str]:
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def write_json_file(*, file_name: str, path: str, json_data: dict) -> None:
    create_path_if_not_exist(path=path)

    with open(f'{path}{file_name}', 'w') as f:
        f.write(json.dumps(json_data, indent=4))
