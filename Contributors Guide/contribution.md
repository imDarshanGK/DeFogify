# Contributing To DeFogify

This documentation guides you in the contribution process.

## Submitting Contributions👩‍💻


### 1️⃣ Fork the project

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

### 2️⃣ Work on feature/fixes

- Follow the [Installation instruction](https://github.com/gitgoap/DeFogify#installation) to set up your environment.
- Implement the features/fixes.
- After you are done making changes, add the files to git:
```bash
# To add all new files to the working branch.
git add .
# To add files selectively to the working branch
git file1 file2 file3
```

### 3️⃣ Commit

commit the changes with:
```bash
# This message gets associated with every file in your commit
git commit -m "descriptive message"  
```
Add a descriptive message for convenience of the reviewer.

**Note:** Squash multiple commits into one for a clean pull request.

### 4️⃣ Push Changes

Upload your changes to your fork from local:
```bash
git push -u origin branch_name
```

### 5️⃣ Pull Request

- Create a Pull Request from your fork
	 `Contribute` -> `Open Pull Request` 
	which will be reviewed and suggestions for improvements.
- Provide a clear title and description linking the associated issue, helps reviewers know context of the Pull Request.

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
