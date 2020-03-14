# Introduction
Tsu :snowflake: is cloud native, open source blogging software designed with extensibility and back-end developer experience in mind.

## Tenets
- Put learning first.
  Our goal is come away with software we can both use as a learning tool to explore cloud native architectures and for its intended purpose (as blogging software).  
- Leverage cloud native architectures and tools.
- Prioritize back-end developer experience.
- Be opinionated in initial design choices while leaving space for maximum configurability and flexibility.

## Features
- Minimal UI, emphasis on back-end.
- Production ready and thoroughly documented.
- Platform and tool agnostic in final state..

# Dev Commands
(`tsu.bat` instead of `./tsu` to call CLI tool on Windows)
- `./tsu publish posts\vocab-app-launch.tsu` to publish post
- `./tsu deploy` after updating template/code

# Prod Commands
- `./tsu -s prod publish posts\vocab-app-launch.tsu` to publish post
- `./tsu -s prod deploy` after updting template/code

## Getting Started
- config.yml setup
  - Make a copy of config.example.yml and rename as config.yml. Set domain names to your desired domain names.
  - Generate a domain certification in AWS Certificate Manager and set domain_cert to the certificate ARN (ex, `{arn:aws:acm:region:id:certificate/id}`)
  - The `default` config is intended for staging. The CLI deploy command will deploy to the staging config unless the `--stage prod` flag is passed.
- Deploy staging with serverless framework
  - Use tsu deploy CLI command to create the CloudFormation stack using serverless framework
  - The stack will take ~30 min. on first deploy to initialize the CloudFront CDN.
- Write posts
- Customize CSS/template
- Deploy prod

## Updating Forks
```
git fetch upstream master
git merge upstream/master
```
