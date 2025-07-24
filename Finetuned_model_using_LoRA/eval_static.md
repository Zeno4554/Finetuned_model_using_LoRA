# Static Evaluation Results

## Base vs. Fine-tuned Model Comparison

### Task 1: Create a new Git branch and switch to it

**Base Model Response:**
```
To create a new Git branch and switch to it, you can use the following command:

```
git checkout -b <branch-name>
```

Replace `<branch-name>` with a name for your new branch.

Once you have created the branch, you can switch to it by running the following command:

```
git checkout <branch-name>
```

Replace `<branch-name>` with the name of the branch you want to switch
```

**Fine-tuned Model Response:**
```
To create a new Git branch and switch to it, you can use the following command:

```
git checkout -b <branch_name>
```

Replace `<branch_name>` with a name for your new branch.

For example:

```
git checkout -b my-new-branch
```

Switch to the new branch by running the following command:

```
git checkout master
```

Replace `master` with the name
```

**Metrics:**
- BLEU: 0.5358
- ROUGE-L: 0.7438
- Plan Quality: 1

---

### Task 2: Compress the folder reports into reports.tar.gz

**Base Model Response:**
```
To compress the folder reports into reports.tar.gz, you can use the following command:

```
tar -czvf reports.tar.gz reports
```

This command creates a compressed archive named reports.tar.gz containing the contents of the reports folder. The `-czvf` option specifies the compression type (tar.gz), `-vf` specifies the compression level (verbose), and `-` specifies the output file name.
```

**Fine-tuned Model Response:**
```
To compress the folder reports into reports.tar.gz, you can use the following command:

```
cd reports
tar czf reports.tar.gz reports
```

This command creates a compressed archive named reports.tar.gz containing all the files in the current directory.
```

**Metrics:**
- BLEU: 0.4111
- ROUGE-L: 0.66
- Plan Quality: 1

---

### Task 3: List all Python files in the current directory recursively

**Base Model Response:**
```
Here's a Python script that lists all Python files in the current directory recursively:

```python
import os

def list_files(path):
    files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            files.append(os.path.join(root, file))
    return files

def main():
    files = list_files('.')
    print(
```

**Fine-tuned Model Response:**
```
Here's a Python script that lists all Python files in the current directory recursively:

```python
import os

def list_files(path):
    files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            files.append(os.path.join(root, file))
    return files

print(list_files('.'))
```

This script uses the `
```

**Metrics:**
- BLEU: 0.8312
- ROUGE-L: 0.9109
- Plan Quality: 1

---

### Task 4: Set up a virtual environment and install requests

**Base Model Response:**
```
To set up a virtual environment and install requests, follow these steps:

1. Open a command prompt or terminal window.
2. Type the following command to create a new virtual environment:

   ```
   python -m venv myenv
   ```

3. Activate the virtual environment by running the following command:

   ```
   source myenv/bin/activate
   ```

4. Install requests using pip:
```

**Fine-tuned Model Response:**
```
To set up a virtual environment and install requests, follow these steps:

1. Open a command prompt or terminal window.
2. Type the following command to create a new virtual environment:

   ```
   python -m venv my_env
   ```

3. Activate the virtual environment by running the following command:

   ```
   source my_env/bin/activate
   ```

4. Install requests using pip:
```

**Metrics:**
- BLEU: 0.9064
- ROUGE-L: 0.9455
- Plan Quality: 1

---

### Task 5: Fetch only the first ten lines of a file named output.log

**Base Model Response:**
```
To fetch only the first ten lines of a file named output.log, you can use the `head` command with the `-n` option. Here's an example:

```
$ head -n 10 output.log
```

This command will display the first 10 lines of the output.log file.
```

**Fine-tuned Model Response:**
```
To fetch only the first ten lines of a file named output.log, you can use the `head` command with the `-n` option. Here's an example:

```
$ head -n 10 output.log
```

This command will display the first ten lines of the output.log file.
```

**Metrics:**
- BLEU: 0.94
- ROUGE-L: 0.9778
- Plan Quality: 1

---

### Task 6: Find all files modified in the last 24 hours and copy them to backup/

**Base Model Response:**
```
To find all files modified in the last 24 hours and copy them to backup/ directory, you can use the following command:

```
find . -type f -mtime +24 -exec cp {} backup/ \;
```

Replace `backup/` with the desired backup directory path.

This command will find all files modified in the last 24 hours and copy them to the backup directory.
```

**Fine-tuned Model Response:**
```
To find all files modified in the last 24 hours and copy them to backup/ directory, you can use the following command:

```
find . -type f -mtime +24 -exec cp {} backup/ \;
```

Replace `backup/` with the desired backup directory path.

This command will find all files modified in the last 24 hours and copy them to the backup directory.
```

**Metrics:**
- BLEU: 1.0
- ROUGE-L: 1.0
- Plan Quality: 2

---

### Task 7: Show the number of running Docker containers and their names

**Base Model Response:**
```
Here's the output of the `docker ps` command with the number of running containers and their names:

```
CONTAINER ID        IMAGE
```

**Fine-tuned Model Response:**
```
To show the number of running Docker containers and their names, you can use the following command:

```
docker ps -a
```

This command will list all running Docker containers, including their names. You can use the `-a` flag to show all containers, or the `--all` flag to show all containers, including those that are not running.

Here's an example output:

```
CONTAINER ID        IMAGE
```

**Metrics:**
- BLEU: 0.0927
- ROUGE-L: 0.3095
- Plan Quality: 1

## Summary Statistics

| Task | BLEU Score | ROUGE-L Score | Plan Quality |
|------|------------|---------------|--------------|
| Git branch creation | 0.5358 | 0.7438 | 1 |
| File compression | 0.4111 | 0.66 | 1 |
| Python file listing | 0.8312 | 0.9109 | 1 |
| Virtual environment setup | 0.9064 | 0.9455 | 1 |
| File head command | 0.94 | 0.9778 | 1 |
| File modification search | 1.0 | 1.0 | 2 |
| Docker container listing | 0.0927 | 0.3095 | 1 |

**Average Scores:**
- BLEU: 0.6739
- ROUGE-L: 0.7868
- Plan Quality: 1.14