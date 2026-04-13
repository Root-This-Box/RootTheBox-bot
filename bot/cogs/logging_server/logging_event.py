import discord
from discord.ext import commands

voice_id = 1492714355513622588
message_id = 1492714356247498772
join_leave_channel_id = 1492714360974606338
member_id = 1492714362555600896
server_id = 1492714363293798420

class LoggingEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # joining and leaving
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(join_leave_channel_id)
        
        member_count = sum(1 for m in member.guild.members if not m.bot)

        embed = discord.Embed(
            title=f"Member Joined {member.name}",
            description="**Member Joined**",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        #avatar cuz we fancy like dat
        embed.set_thumbnail(url=member.display_avatar.url if member.display_avatar else member.default_avatar.url)

        embed.add_field(
            name="User",
            value=f"{member.mention} ({member.id})",
            inline=False
        )

        embed.add_field(
            name="Member Count",
            value=f"{member_count}th member to join",
            inline=False
        )

        embed.add_field(
            name="Account Created",
            value=discord.utils.format_dt(member.created_at, style='F'),
            inline=False
        )
        if channel:
            await channel.send(embed=embed)
        else:
            print(f"Join/Leave channel with ID {join_leave_channel_id} not found.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(join_leave_channel_id)

        if member.joined_at is not None:
            time_stayed = discord.utils.utcnow() - member.joined_at

            days = time_stayed.days
            hours, remainder = divmod(time_stayed.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            stayed_str = f"{days}d {hours}h {minutes}min"
        else:
            stayed_str = "Unknown"

        embed = discord.Embed(
            title=f"{member.name}",
            description="**Member Left**",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, style='F'), inline=False)
        embed.add_field(name="Time Stayed", value=stayed_str, inline=False)

        if channel:
            await channel.send(embed=embed)
        else:
            print(f"Join/Leave channel with ID {join_leave_channel_id} not found.")

    # voice state updates
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel = self.bot.get_channel(voice_id)

        if before.channel is None and after.channel is not None:
            # User joined a voice channel
            embed = discord.Embed(
                title=f"{member.name} joined voice channel",
                description=f"**{member.mention} joined {after.channel.mention}**",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
        elif before.channel is not None and after.channel is None:
            # User left a voice channel
            embed = discord.Embed(
                title=f"{member.name} left voice channel",
                description=f"**{member.mention} left {before.channel.mention}**",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
        elif before.channel != after.channel:
            # User switched voice channels
            embed = discord.Embed(
                title=f"{member.name} switched voice channels",
                description=f"**{member.mention} switched from {before.channel.mention} to {after.channel.mention}**",
                color=discord.Color.orange(),
                timestamp=discord.utils.utcnow()
            )
        else:
            return  # No relevant change

        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        if channel:
            await channel.send(embed=embed)
        else:
            print(f"Voice log channel with ID {voice_id} not found.")

    # message edits and deletes
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.bot.get_channel(message_id)

        if before.content == after.content:
            return  # Ignore embeds or other non-content changes

        embed = discord.Embed(
            title=f"{before.author.name} edited a message",
            description=f"**{before.author.mention} edited a message in {before.channel.mention}**",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(name="Before", value=before.content or "*(no content)*", inline=False)
        embed.add_field(name="After", value=after.content or "*(no content)*", inline=False)

        embed.set_thumbnail(url=before.author.avatar.url if before.author.avatar else before.author.default_avatar.url)

        if channel:
            await channel.send(embed=embed)
        else:
            print(f"Message log channel with ID {message_id} not found.")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(message_id)

        embed = discord.Embed(
            title=f"{message.author.name} deleted a message",
            description=f"**{message.author.mention} deleted a message in {message.channel.mention}**",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(name="Content", value=message.content or "*(no content)*", inline=False)

        embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)

        if channel:
            await channel.send(embed=embed)
        else:
            print(f"Message log channel with ID {message_id} not found.")

    # server updates
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        channel = self.bot.get_channel(server_id)
        if channel is None:
            return

        changes = []

        # Basic identity
        if before.name != after.name:
            changes.append(f"**Name:** {before.name} → {after.name}")

        if before.description != after.description:
            changes.append(f"**Description:** {before.description or 'None'} → {after.description or 'None'}")

        if before.icon != after.icon:
            changes.append("**Icon changed**")

        if before.banner != after.banner:
            changes.append("**Banner changed**")

        if before.splash != after.splash:
            changes.append("**Splash image changed**")

        if before.discovery_splash != after.discovery_splash:
            changes.append("**Discovery splash changed**")

        # Ownership
        if before.owner_id != after.owner_id:
            changes.append(f"**Owner:** <@{before.owner_id}> → <@{after.owner_id}>")

        # Channels
        if before.afk_channel != after.afk_channel:
            changes.append(f"**AFK Channel:** {before.afk_channel} → {after.afk_channel}")

        if before.afk_timeout != after.afk_timeout:
            changes.append(f"**AFK Timeout:** {before.afk_timeout}s → {after.afk_timeout}s")

        if before.system_channel != after.system_channel:
            changes.append(f"**System Channel:** {before.system_channel} → {after.system_channel}")

        if before.rules_channel != after.rules_channel:
            changes.append(f"**Rules Channel:** {before.rules_channel} → {after.rules_channel}")

        if before.public_updates_channel != after.public_updates_channel:
            changes.append(f"**Community Updates Channel:** {before.public_updates_channel} → {after.public_updates_channel}")

        # Server settings
        if before.verification_level != after.verification_level:
            changes.append(f"**Verification Level:** {before.verification_level} → {after.verification_level}")

        if before.explicit_content_filter != after.explicit_content_filter:
            changes.append(f"**Content Filter:** {before.explicit_content_filter} → {after.explicit_content_filter}")

        if before.default_notifications != after.default_notifications:
            changes.append(f"**Default Notifications:** {before.default_notifications} → {after.default_notifications}")

        if before.mfa_level != after.mfa_level:
            changes.append(f"**MFA Level:** {before.mfa_level} → {after.mfa_level}")

        if before.preferred_locale != after.preferred_locale:
            changes.append(f"**Locale:** {before.preferred_locale} → {after.preferred_locale}")

        # Boosting
        if before.premium_tier != after.premium_tier:
            changes.append(f"**Boost Tier:** {before.premium_tier} → {after.premium_tier}")

        if before.premium_subscription_count != after.premium_subscription_count:
            changes.append(f"**Boost Count:** {before.premium_subscription_count} → {after.premium_subscription_count}")

        # Features
        if before.features != after.features:
            removed = set(before.features) - set(after.features)
            added = set(after.features) - set(before.features)

            if added:
                changes.append(f"**Features Added:** {', '.join(added)}")
            if removed:
                changes.append(f"**Features Removed:** {', '.join(removed)}")

        # Vanity URL
        if before.vanity_url_code != after.vanity_url_code:
            changes.append(f"**Vanity URL:** {before.vanity_url_code} → {after.vanity_url_code}")

        # NSFW level
        if before.nsfw_level != after.nsfw_level:
            changes.append(f"**NSFW Level:** {before.nsfw_level} → {after.nsfw_level}")

        # Safety alerts channel
        if before.safety_alerts_channel != after.safety_alerts_channel:
            changes.append(f"**Safety Alerts Channel:** {before.safety_alerts_channel} → {after.safety_alerts_channel}")

        # If nothing changed
        if not changes:
            return

        embed = discord.Embed(
            title=f"{before.name} Updated",
            description="\n".join(changes),
            color=discord.Color.purple(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=after.icon.url if after.icon else None)

        await channel.send(embed=embed)
    
    # member updates
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel = self.bot.get_channel(member_id)
        if channel is None:
            return

        changes = []

        if before.display_name != after.display_name:
            changes.append(f"**Display Name:** {before.display_name} → {after.display_name}")

        if before.roles != after.roles:
            removed = set(before.roles) - set(after.roles)
            added = set(after.roles) - set(before.roles)

            if added:
                changes.append(f"**Roles Added:** {', '.join(role.name for role in added)}")
            if removed:
                changes.append(f"**Roles Removed:** {', '.join(role.name for role in removed)}")

        if before.nick != after.nick:
            changes.append(f"**Nickname:** {before.nick} → {after.nick}")

        if before.avatar != after.avatar:
            changes.append("**Avatar changed**")

        if not changes:
            return

        embed = discord.Embed(
            title=f"{before.name} Updated",
            description="\n".join(changes),
            color=discord.Color.teal(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=after.avatar.url if after.avatar else after.default_avatar.url)

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LoggingEvent(bot))