#![windows_subsystem = "windows"]

use wry::WebViewBuilder;
use winit::{
    application::ApplicationHandler,
    event::WindowEvent,
    event_loop::{ActiveEventLoop, EventLoop},
    window::{Window, WindowId, Icon},
    dpi::LogicalSize,
};

#[derive(Default)]
struct App {
    window: Option<Window>,
    _webview: Option<wry::WebView>,
}

impl ApplicationHandler for App {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        let img = image::open("assets/logo.png").unwrap().into_rgba8();
        let (w, h) = img.dimensions();
        let icon = Icon::from_rgba(img.into_raw(), w, h).unwrap();

        let window = event_loop.create_window(
            Window::default_attributes()
                .with_title("D# Wiki")
                .with_inner_size(LogicalSize::new(1200, 700))
                .with_window_icon(Some(icon))
        ).unwrap();

        let webview = WebViewBuilder::new()
            .with_url("https://dajdon.hu/dsharp/wiki.html")
            .build(&window)
            .unwrap();

        self._webview = Some(webview);
        self.window = Some(window);
    }

    fn window_event(&mut self, event_loop: &ActiveEventLoop, _id: WindowId, event: WindowEvent) {
        if let WindowEvent::CloseRequested = event {
            event_loop.exit();
        }
    }
}

fn main() {
    let event_loop = EventLoop::new().unwrap();
    let mut app = App::default();
    event_loop.run_app(&mut app).unwrap();
}