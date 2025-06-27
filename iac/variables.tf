variable "RENDER_API_KEY" {
  description = "The Render api key"
  type        = string
  sensitive   = true
}

variable "RENDER_OWNER_ID" {
  description = "The Render owner id"
  type        = string
  sensitive   = true
}

variable "DISCORD_TOKEN" {
  description = "The Discord bot token"
  type        = string
  sensitive   = true
}

variable "APP_ID" {
  description = "The app id"
  type        = string
  sensitive   = true
}

variable "PUBLIC_KEY" {
  description = "The public key"
  type        = string
  sensitive   = true
}

variable "GUILD_ID" {
  description = "The guild id"
  type        = string
  sensitive   = true
}