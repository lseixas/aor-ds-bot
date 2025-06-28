
terraform {

  cloud {

    organization = "AfraidORespect"

    workspaces {
      name = "gh-actions-workspace"
    }
  }

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

  name   = "aor-ds-bot"
  plan   = "starter"
  region = "oregon"

  start_command = "printenv && python -m app.main"

  env_vars = {
    "DISCORD_TOKEN" = { value = var.DISCORD_TOKEN }
    "APP_ID"        = { value = var.APP_ID }
    "PUBLIC_KEY"    = { value = var.PUBLIC_KEY }
    "GUILD_ID"      = { value = var.GUILD_ID }
  }

  runtime_source = {
    native_runtime = {
      repo_url      = "https://github.com/lseixas/aor-ds-bot"
      auto_deploy   = true
      branch        = "main"
      build_command = "pip install -r requirements.txt"
      runtime       = "python"
    }
  }
}