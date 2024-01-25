import discord

class Pagination_View(discord.ui.View):
    def __init__(self, req_obj: discord.Interaction, data, server_name, server_kc):
        super().__init__()
        self.req_obj: discord.Interaction = req_obj
        self.data: None = data
        self.server_name: None = server_name
        self.server_kc: None = server_kc
        self.current_page: int = 1
        self.items_per_page: int = 5
        self.first_page = 1
        self.last_page = len(self.data) // self.items_per_page + (len(self.data) % self.items_per_page > 0)
        self.embed = None
        self.button_pressed = False

    @discord.ui.button(label='|<', style=discord.ButtonStyle.primary)
    async def first_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page != self.first_page:
            self.button_pressed = True
            self.current_page = 1
            start_index = 0
            end_index = self.current_page * self.items_per_page
            start_index = end_index - self.items_per_page
            await self.update_embed(self.data[start_index:end_index])

    @discord.ui.button(label='<', style=discord.ButtonStyle.green)
    async def prev_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page != self.first_page:
            self.button_pressed = True
            self.current_page -= 1
            end_index = self.current_page * self.items_per_page
            start_index = end_index - self.items_per_page
            await self.update_embed(self.data[start_index:end_index])

    @discord.ui.button(label='>', style=discord.ButtonStyle.green)
    async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page != self.last_page:
            self.button_pressed = True
            self.current_page += 1
            end_index = self.current_page * self.items_per_page
            start_index = end_index - self.items_per_page
            await self.update_embed(self.data[start_index:end_index])

    @discord.ui.button(label='>|', style=discord.ButtonStyle.primary)
    async def last_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page != self.last_page:
            self.button_pressed = True
            self.current_page = self.last_page
            end_index = self.current_page * self.items_per_page
            start_index = end_index - self.items_per_page
            await self.update_embed(self.data[start_index:])

    def create_embed(self, data):
        card = discord.Embed(title=f"{self.server_name}'s Team Kill History",
                             description=f"Kill Count: {len(self.data)}", color=discord.Color.random())
        for item in data:
            kill_id = item[0]
            killer_id = item[1]
            victim_id = item[2]
            kill_datetime = item[3].strftime("%m/%d/%y @ %I:%M %p")
            note = item[4]
            if note is not None:
                card.add_field(name=f"ID: {kill_id} - {kill_datetime}",
                               value=f"<@{killer_id}> brutally murdered <@{victim_id}>. **Note:** {note}", inline=False)
            else:
                card.add_field(name=f"ID: {kill_id} - {kill_datetime}",
                               value=f"<@{killer_id}> brutally murdered <@{victim_id}>.", inline=False)
        if self.button_pressed:
            card.add_field(name=f"Page {self.current_page}", value="*The interaction didn't fail. It's lying to you...*", inline=False)
        else:
            card.add_field(name=f"Page {self.current_page}",
                           value="", inline=False)
        self.embed = card
        return card

    async def display_embed(self):
        try:
            self.create_embed(self.data[:5])
            await self.req_obj.response.send_message(embed=self.embed, view=self)
        except Exception as e:
            # Print the exception for debugging purposes
            print(f"Error in display_embed: {e}")
            self.embed = None  # Set self.embed to None in case of an error

        if self.embed is None:
            print("Error: self.embed is None in display_embed")

    async def update_embed(self, data):
        await self.req_obj.edit_original_response(embed=self.create_embed(data), view=self)

    def get_req(self):
        return self.req_obj

    def get_data(self):
        return self.data

    def get_server_name(self):
        return self.server_name

    def get_server_kc(self):
        return self.server_kc

    def get_current_page(self):
        return self.current_page

    def get_items_per_page(self):
        return self.items_per_page

    def set_req_obj(self, req_obj: discord.Interaction):
        self.req_obj = req_obj

    def set_data(self, data):
        self.data = data

    def set_server_name(self, server_name):
        self.server_name = server_name

    def set_server_kc(self, kc: int):
        self.server_kc = kc

    def set_current_page(self, current_page: int):
        self.current_page = current_page

    def set_items_per_page(self, items_per_page: int):
        self.items_per_page = items_per_page
