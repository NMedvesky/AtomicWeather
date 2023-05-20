import tkinter
import customtkinter

# Get weather Data
from weatherGov import Weather

customtkinter.set_widget_scaling(1)  # widget dimensions and text size
customtkinter.set_window_scaling(1)  # window geometry dimensions

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):
	def __init__(self):
		super().__init__()

		self.WIDTH = self.winfo_screenwidth()/4.5
		self.HEIGHT = self.winfo_screenheight()/2

		newForecast = Weather()

		newForecast.getWeather()
		newForecast.formatForecast()

		date = newForecast.forecast[0]["date"]["formatedDate"]

		self.title(f"Hourly Weather | {date}")
		self.geometry(f"{int(self.WIDTH)}x{int(self.HEIGHT)}")
		self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed


		self.frame_center = customtkinter.CTkFrame(master=self,
												   width=self.WIDTH*0.9,
												   height=self.HEIGHT*0.1,
												   #fg_color="default_theme",
												   corner_radius=30)
		self.frame_center.grid(padx=self.WIDTH*0.05, pady=self.HEIGHT*0.03)
		self.city = customtkinter.CTkLabel(master=self.frame_center,
												  width=self.WIDTH*0.5,
												  height=self.HEIGHT*0.05,
												  fg_color="#404040",
												  text=newForecast.forecast[0]["city"],
												  font=customtkinter.CTkFont(size=25))
		self.city.grid(padx=self.WIDTH*0.05, pady=self.HEIGHT*0.02)

		index = 0
		for i in range(4):
			forecast = newForecast.forecast[index]
			forecastText = f"{forecast['date']['hour']}    |    {forecast['temp']}°{forecast['tempUnit']}    |    {forecast['windSpeed']} mph\n{forecast['forecastDesc']}"

			self.generalInfoFrame = customtkinter.CTkFrame(master=self.frame_center,
												  	  width=self.WIDTH*0.8,
												  	  height=self.HEIGHT*0.15,
												  	  fg_color="#404040",
												  	  border_color="#4cff79",
												  	  border_width=self.WIDTH*0.005)
			self.generalInfoFrame.grid(padx=self.WIDTH*0.05, pady=self.WIDTH*0.025)

			self.generalInfo = customtkinter.CTkLabel(master=self.generalInfoFrame,
												  	  width=self.WIDTH*0.8,
												  	  height=self.HEIGHT*0.15,
												  	  fg_color="#404040",
												  	  text=forecastText,
												  	  font=customtkinter.CTkFont(size=20))
			self.generalInfo.grid(padx=self.WIDTH*0.01, pady=self.HEIGHT*0.01)

			index += 3


	def on_closing(self, event=0):
			self.destroy()


if __name__ == "__main__":
	app = App()
	app.mainloop()