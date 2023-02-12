# We're building lightweight blogging software

Tsu ❄️ is open source, serverless, and highly extensible. It can be used with any front end framework. Posts are stored as flat HTML files, making Tsu blogs fast and SEO optimized.

Made with Tsu:
- [emshea.com](emshea.com)
- [rsyvarth.com](rsyvarth.com)

# Getting Started
- Make a fork of this repo
- config.yml setup
  - Make a copy of config.example.yml and rename as config.yml. Set domain names to your desired domain names.
  - Generate a domain certification in AWS Certificate Manager and set domain_cert to the certificate ARN (ex, `{arn:aws:acm:region:id:certificate/id}`)
  - The `default` config is intended for staging. The CLI deploy command will deploy to the staging config unless the `--stage prod` flag is passed.
- Deploy staging with serverless framework
  - Use `./tsu deploy` CLI command to create the CloudFormation stack using serverless framework
  - The stack will take ~30 min. on first deploy to initialize the CloudFront CDN.
- Customize CSS / template
  - You can override any template / css by adding files into the `/custom` directory
- Write posts in the `/posts` directory

## Google Photos generate
-- `./tsu generate '{name of Google Photos album}'`
<!-- page through images within one hour of generating -->
<!-- to add a different header image, create a folder and add the downloaded photo to it. Reference the file path (./folder_name/image_name.jpg) -->

## Dev Commands
(`tsu.bat` instead of `./tsu` to call CLI tool on Windows)
- `./tsu deploy` to update server side code after updating templates/code
- `./tsu publish posts/vocab-app-launch.tsu` to publish post

## Prod Commands
- `./tsu -s prod deploy` to update server side code after updating templates/code
- `./tsu -s prod publish posts/vocab-app-launch.tsu` to publish post
- `./tsu -s prod publish posts/vocab-app-launch.tsu --email` to publish and email to subscribers (there is a confirmation step before sending)

## Updating Tsu
You should periodically update your fork of Tsu against the main repo to get the
latest features / bug fixes. To do this, run the following command:
```
./tsu update
```
