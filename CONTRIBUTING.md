# 🌍 Contributing.

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

## 👶 Getting Started!

Ready to contribute? Here's how to set up `brave-chat-server` for local development.

1. Fork the `brave-chat-server` repo on GitHub.
2. Clone your fork locally:

```sh
git clone git@github.com:your_name_here/brave-chat-server.git
```

3. Follow the instructions listed under the [`Installation with Make`](https://github.com/brave-chat/brave-chat-server#installation-with-make) section of the readme file to set up your dev environment.

4. Create a branch for local development:

```sh
git checkout -b name-of-your-bugfix-or-feature
```

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass tox tests, including testing other Python versions with make:

```sh
make test-all
```

6. Commit your changes and push your branch to GitHub:

```sh
git add .
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

7. Submit a pull request through the GitHub website.

## 📙 Pull Request Guidelines.

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests, if possible.
2. The pull request should work for Python 3.9.10. Check and make sure that the tests pass for all supported Python versions.

## 💡 Tips.

To run a subset of tests:

```sh
make test
make lint
make coverage
```

Thank you for helping us improve!
