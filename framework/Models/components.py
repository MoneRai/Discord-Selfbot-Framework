class MessageComponent:
    def __new__(cls, _, **data):
        order = {
            1: ActionRow,
            2: Button,
            3: StringSelect,
            4: TextInput,
            5: UserSelect,
            6: RoleSelect,
            7: MentionableSelect,
            8: ChannelSelect
        }
        return order[data.get("type")](_, **data)

    def __init__(self, message, **data):
        self.message = message
        self.disabled: bool = data.get("disabled")
        self.custom_id: str = data.get("custom_id")

class ActionRow:
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    
    def __init__(self, message, **data):
        self.type: int = int(data.get("type", 1))
        self.components: list = ([MessageComponent(message, **d) for d in data.get("components")]) if data.get("components") else []

class Button(MessageComponent):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
        
    def __init__(self, message, **data):
        self.message = message
        self.type: int = data.get("type", 1)
        self.style: int = int(data.get("style", 1))
        self.label: str = data.get("label")
        self.emoji: str = data.get("emoji")
        self.url: str = data.get("url")
        self.custom_id = data.get("custom_id")

    async def click(self):
        return await self.message.parent.click_button(self)

class SelectMenu(MessageComponent):
    def __new__(cls, _, **data):
        order = {
            3: StringSelect,
            5: UserSelect,
            6: RoleSelect,
            7: MentionableSelect,
            8: ChannelSelect
        }
        return order[data.get("type")](_, **data)

    def __init__(self, message, **data):
        self.message = message
        self.placeholder: str = data.get("placeholder")
        self.min_values: int = int(data.get("min_values", 1))
        self.max_values: int = int(data.get("max_values", 1))
        self.options: list = (SelectOption(**d) for d in data.get("options"))
        self.default_values: list = data.get("default_values")
        self.custom_id: str = data.get("custom_id")

    async def select(self, values: list):
        return await self.message.parent.response_select(self, values)

class StringSelect(SelectMenu):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    
    def __init__(self, message, **data):
        super().__init__(message, **data)
        self.type: int = data.get("type", 3)

class UserSelect(SelectMenu):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    
    def __init__(self, message, **data):
        super().__init__(message, **data)
        self.type: int = data.get("type", 5)

class RoleSelect(SelectMenu):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    
    def __init__(self, message, **data):
        super().__init__(message, **data)
        self.type: int = data.get("type", 6)

class MentionableSelect(SelectMenu):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    
    def __init__(self, message, **data):
        super().__init__(message, **data)
        self.type: int = data.get("type", 7)

class ChannelSelect(SelectMenu):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    
    def __init__(self, message, **data):
        super().__init__(message, **data)
        self.channel_types: list = data.get("channel_types")
        self.type: int = data.get("type", 8)

class SelectOption:
    def __init__(self, **data):
        self.label: str = data.get("label")
        self.value: str = data.get("value")
        self.description: str = data.get("description")
        self.emoji: str = data.get("emoji")
        self.default: str = data.get("default")

class DefaultValue:
    def __init__(self, **data):
        self.type: int = data.get("type")
        self.value: str = data.get("value")

class TextInput:
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, *_, **data):
        self.style: int = int(data.get("style", 1))
        self.label: str = data.get("label")
        self.custom_id: str = data.get("custom_id")
        self.value: str = data.get("value")
        self.placeholder: str = data.get("placeholder")
        self.required: bool = data.get("required")
        self.min_length: int = data.get("min_length")
        self.max_length: int = data.get("max_length")