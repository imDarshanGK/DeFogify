# Contributing To DeFogify

This documentation guides you in the contribution process.

## Submitting Contributions👩‍💻

### 1️⃣ Find an issue
- Browse [Issues](https://github.com/gitgoap/DeFogify/issues) Tab for existing issues or create new ones.
- Wait for the issue to be assigned before starting your work.
- **Note:** Every change needs to have an associated issue.
### 2️⃣ Fork the project

[Fork](https://github.com/gitgoap/DeFogify/fork) the repository, this creates a copy of the repository under your GitHub profile for working:
```bash
# clone your fork locally
git clone https://github.com/<your-username>/DeFogify  
cd DeFogify

# add the original repository as 'upstream' remote
git remote add upstream https://github.com/original-owner/DeFogify  
```  

If you have already forked the project, just update your fork:
```bash
# Fetch and merge the latest updates from upstream
git pull upstream main
git checkout main
git merge upstream/main
git push origin main
```  

Create a new branch before working on a new issue:
```bash
git checkoout -b <new_feature>
```

### 3️⃣ Work on the assigned issue

- Follow the [Installation instruction](https://github.com/gitgoap/DeFogify#installation) to set up your environment.
- Implement the features/fixes.
- After you are done making changes, add the files to git:
```bash
# To add all new files to the working branch.
git add .
# To add files selectively to the working branch
git file1 file2 file3
```

### 4️⃣ Commit

commit the changes with:
```bash
# This message gets associated with every file in your commit
git commit -m "descriptive message"  
```
Add a descriptive message for convenience of the reviewer.

**Note:** Squash multiple commits into one for a clean pull request.

### 5️⃣ Push Changes

Upload your changes to your fork from local:
```bash
git push -u origin branch_name
```

### 6️⃣ Pull Request

- Create a Pull Request from your fork
	 `Contribute` -> `Open Pull Request` 
	which will be reviewed and suggestions for improvements.
- Provide a clear title and description linking the associated issue, helps reviewers know context of the Pull Request.

# Alternatively, using GitHub Desktop 🖥️

### 1️⃣ Fork the Repository

[Fork](https://github.com/gitgoap/DeFogify/fork) the repository on GitHub:
- Open GitHub Desktop and log in to your GitHub account.
- Go to `File` -> `Clone Repository`.
- Select your fork and choose a local path to clone it.
### 2️⃣ Update Your Fork

If you’ve already forked the project, update it before working:
- In GitHub Desktop, click `Fetch origin` and then `Pull origin` if updates are available.
### 3️⃣ Create a Branch

Before making changes, create a branch for the issue:
- Click `Current Branch` -> `New Branch`.
- Enter a descriptive branch name and click `Create Branch`.
### 4️⃣ Make Changes

- Follow the [installation instructions](https://github.com/gitgoap/DeFogify#installation).
- Review changes in GitHub Desktop:
  - Changed files will appear in the left panel.
  - Review specific changes in the right panel.
  - Select files to include in the commit.
### 5️⃣ Commit and Push

- Enter a summary in the "Summary" field and click `Commit to <branch_name>`.
- Push changes to your fork with `Push origin`.
### 6️⃣ Submit a Pull Request

- On GitHub, navigate to your fork and click `Compare & pull request`.
- Add a relevant title, description, and screenshots (if applicable).
- Click `Create pull request`.


> Your Pull Request will be reviewed and merged by the maintainer 🚀

## Need Help?🤔
You can refer to the following articles on the basics of Git and GitHub and also contact the Project Mentors, in case you are stuck:

- [Watch this video to get started, if you have no clue about open source](https://youtu.be/SYtPC9tHYyQ)
- [Forking a Repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
- [Cloning a Repo](https://help.github.com/en/desktop/contributing-to-projects/creating-a-pull-request)
- [How to create a Pull Request](https://opensource.com/article/19/7/create-pull-request-github)
- [Getting started with Git and GitHub](https://towardsdatascience.com/getting-started-with-git-and-github-6fcd0f2d4ac6)
- [GitHub Desktop]([Getting started with GitHub Desktop - GitHub Docs](https://docs.github.com/en/desktop/overview/getting-started-with-github-desktop))
- [Learn GitHub from Scratch](https://lab.github.com/githubtraining/introduction-to-github)

Hope you will learn something new while contributing to this project!!
