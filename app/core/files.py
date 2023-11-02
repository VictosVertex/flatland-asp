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
