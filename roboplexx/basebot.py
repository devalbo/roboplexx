__author__ = 'ajb'

class BaseBot:

    def initialize_host(self):
        self.host.register_self_rpx_props_and_commands()
        for device in self.devices:
            self.host.register_device(device)

    def initialize_devices(self):
        for device in self.devices:
            device.activate()

    def listen_command_queue(self, command_queue_url):
        self.host.listen_command_queue(command_queue_url)

    def run_web_app(self, ):
        def do_web_app():
            from roboplexx import app
            app.run_web_app()

        from threading import Thread
        thread = Thread(target=do_web_app)
        thread.start()
        print "Web app started"

    def register_with_web_app(self, web_app_url):
        return self.host.register_with_webapp(web_app_url)

    def checkin_with_web_app(self, web_app_url):
        return self.host.checkin_with_web_app(web_app_url)