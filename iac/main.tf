
terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "1.2.0"
    }
  }
}

provider "render" {
  api_key  = var.RENDER_API_KEY
  owner_id = var.RENDER_OWNER_ID
}


resource "render_background_worker" "resource-aor-ds-bot" {

  name   = "git-background-worker"
  plan   = "starter"
  region = "oregon"

  start_command = "python -m app.main"

  env_vars = {
    "DISCORD_TOKEN" = var.DISCORD_TOKEN
    "APP_ID"        = var.APP_ID
    "PUBLIC_KEY"    = var.PUBLIC_KEY
    "GUILD_ID"      = var.GUILD_ID
  }

  runtime_source = {

      auto_deploy   = true
      branch        = "main"
      build_command = "pip install -r requirements.txt"
      repo_url      = "https://www.github.com/lseixas/aor-ds-bot"
      runtime       = "python"
  
  }
  
}