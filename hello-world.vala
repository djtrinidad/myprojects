using Gtk;
using Gdk;

class Desklet : Window {
    public Desklet() {
        // Set up the window (desklet)
        set_default_size(300, 150);
        set_decorated(false);  // No title bar or borders
        set_resizable(false);
        set_app_paintable(true);  // Allows custom drawing

        // Ensure the window is movable
        add_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_MOTION_MASK);

        // Connect signals for moving the window
        this.button_press_event.connect(on_button_press_event);
        this.motion_notify_event.connect(on_motion_notify_event);

        // Set a blue background for the desklet
        this.set_css_name("desklet");
        var css_provider = new CssProvider();
        css_provider.load_from_data("""
            window.desklet {
                background-color: #0000FF;
            }
        """);
        var style_context = this.get_style_context();
        style_context.add_provider(css_provider, GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);
        
        // Basic label for "Hello World"
        var label = new Label("Hello, World!");
        var box = new Box(Orientation.VERTICAL, 10);
        box.append(label);
        set_child(box);

        show();
    }

    // Variables to keep track of drag position
    int start_x = 0;
    int start_y = 0;

    // On button press, record position
    bool on_button_press_event(EventButton event) {
        if (event.button == Gdk.BUTTON_PRIMARY) {
            start_x = (int) event.x_root;
            start_y = (int) event.y_root;
        }
        return false;
    }

    // On motion, move window based on new position
    bool on_motion_notify_event(EventMotion event) {
        if (event.state & Gdk.ModifierType.BUTTON1_MASK != 0) {
            int current_x, current_y;
            get_position(out current_x, out current_y);

            int delta_x = (int) event.x_root - start_x;
            int delta_y = (int) event.y_root - start_y;

            move(current_x + delta_x, current_y + delta_y);

            start_x = (int) event.x_root;
            start_y = (int) event.y_root;
        }
        return false;
    }
}

int main(string[] args) {
    // Initialize GTK application
    var app = new Application("com.example.desklet", ApplicationFlags.FLAGS_NONE);
    app.activate.connect(() => {
        var desklet = new Desklet();
        desklet.present();
    });
    return app.run(args);
}
