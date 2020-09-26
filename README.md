# We're building lightweight blogging software

Tsu ❄️ is open source, serverless, and highly extensible. It can be used with any front end framework. Posts are stored as flat HTML files, making Tsu blogs fast and SEO optimized.

Made with Tsu:
- [emshea.com](emshea.com)
- [rsyvarth.com](rsyvarth.com)

# Getting Started
- config.yml setup
  - Make a copy of config.example.yml and rename as config.yml. Set domain names to your desired domain names.
  - Generate a domain certification in AWS Certificate Manager and set domain_cert to the certificate ARN (ex, `{arn:aws:acm:region:id:certificate/id}`) 
  - The `default` config is intended for staging. The CLI deploy command will deploy to the staging config unless the `--stage prod` flag is passed.
- Deploy staging with serverless framework
  - Use tsu deploy CLI command to create the CloudFormation stack using serverless framework
  - The stack will take ~30 min. on first deploy to initialize the CloudFront CDN.
- Write posts.
- Customize CSS/template.
- Deploy prod.

## Dev Commands
(`tsu.bat` instead of `./tsu` to call CLI tool on Windows)
- `./tsu publish posts\vocab-app-launch.tsu` to publish post
- `./tsu deploy` after updating template/code

## Prod Commands
- `./tsu -s prod publish posts\vocab-app-launch.tsu` to publish post
- `./tsu -s prod deploy` after updting template/code

## Updating Forks
```
git fetch upstream master
git merge upstream/master
```