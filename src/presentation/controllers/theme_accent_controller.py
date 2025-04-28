from presentation.states.dark_mode_state import DarkModeState
from presentation.states.accent_color_state import AccentColorState, AccentColors
from presentation.states.dialogs_state import DialogState, Dialogs
from presentation.states.media_query_state import MediaQueryState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.views.widgets.settings.accent_color_button import AccentColorButton

from flet import *

from presentation.controllers.controller import Controller, Priority

class ThemeAccentController(Controller):
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page
        
        # States
        self.dm_state = DarkModeState()
        self.ac_state = AccentColorState()
        self.dia_state = DialogState()
        self.mq_state = MediaQueryState()
        
        # Event handlers
        self.dm_state.on_change = self.apply_theme_changes
        self.ac_state.on_change = self.apply_accent_changes
        self.dm_state.on_follow_system_change = self.follow_system_change
        self.dia_state.on_done_build = self.update_view
        
        # Initialize client storage if not exists
        self._init_client_storage()
        
    def _init_client_storage(self):
        """Initialize client storage with default values if not set"""
        if not self.page.client_storage.contains_key("dark_mode"):
            self.page.client_storage.set("dark_mode", False)  # Default to Light Mode
            
        if not self.page.client_storage.contains_key("follow_sysdark_mode"):
            self.page.client_storage.set("follow_sysdark_mode", False)  # Default to Manual
            
        if not self.page.client_storage.contains_key("accent_color"):
            self.page.client_storage.set("accent_color", AccentColors.SORA.name)  # Default accent color
    
    def update_view(self):
        """Update view when settings dialog is built"""
        if self.dia_state.done_build == Dialogs.SETTINGS:
            # Load values from client storage
            self.dm_state.active = bool(self.page.client_storage.get("dark_mode"))
            self.dm_state.follow_system_active = bool(self.page.client_storage.get("follow_sysdark_mode"))
            
            # Load accent color
            stored_accent = self.page.client_storage.get("accent_color")
            for color in AccentColors:
                if color.name == stored_accent:
                    self.ac_state.active = color
                    break
    
    def follow_system_change(self):
        """Handle system theme change toggle"""
        active = self.dm_state.follow_system_active
        
        # Apply theme mode based on system or manual setting
        if active:
            self.page.theme_mode = ThemeMode.SYSTEM
        else:
            is_dark = bool(self.page.client_storage.get("dark_mode"))
            self.page.theme_mode = ThemeMode.DARK if is_dark else ThemeMode.LIGHT
        
        # Save to client storage
        self.page.client_storage.set("follow_sysdark_mode", active)
        
        # Update UI
        self.page.update()
    
    def apply_theme_changes(self):
        """Apply theme changes across the application"""
        is_dark_mode = self.dm_state.active
        
        # Update theme mode buttons
        group_id = "theme_mode"
        for button in SettingsImageButton.refs.get(group_id, []):
            is_active = (button.text == "Dark" and is_dark_mode) or (button.text == "Default" and not is_dark_mode)
            self._update_theme_button_style(button, is_active)
        
        # Apply theme mode
        follow_system = bool(self.page.client_storage.get("follow_sysdark_mode"))
        if not follow_system:
            self.page.theme_mode = ThemeMode.DARK if is_dark_mode else ThemeMode.LIGHT
            self.page.update()
        
        # Save to client storage
        self.page.client_storage.set("dark_mode", is_dark_mode)
        
        # Apply accent color with the new theme
        self.apply_accent_changes()
    
    def _update_theme_button_style(self, button, is_active):
        """Update theme button styling based on active state"""
        accent_color = self.ac_state.active.value if hasattr(self.ac_state, 'active') else "#4d191f51"
        
        if is_active:
            button.active = True
            button.bgcolor = accent_color
            button.check_box.bgcolor = self._get_stronger_accent_color(accent_color)
            button.border = border.all(1, self._get_border_color(accent_color))
            button.label.weight = FontWeight.BOLD
        else:
            button.active = False
            button.bgcolor = "#00191f51"
            button.check_box.bgcolor = "#00191f51"
            button.border = border.all(1, "#006b6b6b")
            button.label.weight = FontWeight.NORMAL
        
        button.update()
    
    def apply_accent_changes(self):
        """Apply accent color changes across the application"""
        active_accent = self.ac_state.active
        
        # Update accent color buttons
        for button in AccentColorButton.refs:
            is_active = button.color == active_accent
            self._update_accent_button_style(button, is_active)
        
        # Apply accent color to other UI elements
        self._apply_accent_to_views(active_accent.value)
        
        # Save to client storage
        self.page.client_storage.set("accent_color", active_accent.name)
    
    def _update_accent_button_style(self, button, is_active):
        """Update accent button styling based on active state"""
        if is_active:
            button.active = True
            button.main_content.border = border.all(1.5, Colors.BLACK)
            button.main_content.content.value = "✓"
            button.main_content.content.color = "black"
            button.name_text.weight = FontWeight.W_600
        else:
            button.active = False
            button.main_content.border = border.all(0.5, Colors.BLACK)
            button.main_content.content.value = ""
            button.name_text.weight = FontWeight.W_400
        
        button.main_content.update()
        button.main_content.content.update()
        button.name_text.update()
    
    def _apply_accent_to_views(self, accent_color):
        """Apply accent color to various views and components"""
        # Get references to main views
        from presentation.views.window_view import WindowView
        window_view = None
        
        # Find the WindowView instance in the page
        for control in self.page.controls:
            if isinstance(control, WindowView):
                window_view = control
                break
        
        if not window_view:
            return
        
        # Apply to Start View
        if hasattr(window_view, 'switcher') and window_view.switcher:
            if hasattr(window_view.switcher, 'controls'):
                for view in window_view.switcher.controls:
                    # Start View buttons
                    if hasattr(view, 'new_button') and view.new_button:
                        view.new_button.style.bgcolor = self._get_lighter_accent_color(accent_color)
                        view.new_button.style.side = BorderSide(1, self._get_stronger_accent_color(accent_color))
                        view.new_button.update()
                    
                    if hasattr(view, 'open_button') and view.open_button:
                        view.open_button.style.bgcolor = self._get_lighter_accent_color(accent_color)
                        view.open_button.style.side = BorderSide(1, self._get_stronger_accent_color(accent_color))
                        view.open_button.update()
                    
                    # Apply to search field in Open Existing View
                    if hasattr(view, 'content') and isinstance(view.content, Column):
                        for row in view.content.controls:
                            if isinstance(row, Row):
                                for control in row.controls:
                                    if isinstance(control, TextField) and hasattr(control, 'bgcolor'):
                                        control.bgcolor = self._get_lighter_accent_color(accent_color)
                                        control.update()
        
        # Apply to Sidebar
        if hasattr(window_view, 'sidebar') and window_view.sidebar:
            for button in window_view.sidebar.controls:
                if hasattr(button, 'active') and button.active:
                    button.bgcolor = self._get_lighter_accent_color(accent_color)
                    button.update()
        
        # Update theme buttons with new accent color
        is_dark_mode = self.dm_state.active
        group_id = "theme_mode"
        for button in SettingsImageButton.refs.get(group_id, []):
            is_active = (button.text == "Dark" and is_dark_mode) or (button.text == "Default" and not is_dark_mode)
            self._update_theme_button_style(button, is_active)
    
    def _get_lighter_accent_color(self, color):
        """Get lighter version of accent color for backgrounds"""
        opacity = 0.15  # Lower opacity for lighter effect
        return color.replace("#4d", f"#{int(opacity * 255):02x}")
    
    def _get_stronger_accent_color(self, color):
        """Get stronger version of accent color for highlights"""
        opacity = 0.7  # Higher opacity for stronger effect
        return color.replace("#4d", f"#{int(opacity * 255):02x}")
    
    def _get_border_color(self, color):
        """Extract base color without opacity for borders"""
        return color[3:]  # Remove opacity prefix (#4d)
    
    def apply_initial_theme(self):
        """Apply initial theme and accent colors on application startup"""
        # Load theme settings
        is_dark_mode = bool(self.page.client_storage.get("dark_mode"))
        follow_system = bool(self.page.client_storage.get("follow_sysdark_mode"))
        
        # Set theme mode
        if follow_system:
            self.page.theme_mode = ThemeMode.SYSTEM
        else:
            self.page.theme_mode = ThemeMode.DARK if is_dark_mode else ThemeMode.LIGHT
        
        # Load accent color
        stored_accent = self.page.client_storage.get("accent_color")
        for color in AccentColors:
            if color.name == stored_accent:
                self.ac_state.active = color
                break
        
        # Apply changes
        self.dm_state.active = is_dark_mode
        self.dm_state.follow_system_active = follow_system
        
        self.page.update()
