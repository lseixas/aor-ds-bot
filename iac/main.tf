
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

  runtime_source = {

    env_vars = {
    "DISCORD_TOKEN" = { value = var.DISCORD_TOKEN }
    "APP_ID"        = { value = var.APP_ID }
    "PUBLIC_KEY"    = { value = var.PUBLIC_KEY }
    "GUILD_ID"      = { value = var.GUILD_ID }
    }

    native_runtime = {
      auto_deploy   = true
      branch        = "main"
      build_command = "pip install -r requirements.txt"
      repo_url      = "https://www.github.com/lseixas/aor-ds-bot"
      runtime       = "python"
    }
  }
}