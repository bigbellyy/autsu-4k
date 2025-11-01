from data.generate_files import load_dataset

#config
_generate_dataset = False

if __name__ == "__main__":
    if _generate_dataset:
        load_dataset()