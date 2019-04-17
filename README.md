# LoPy 4 Soil Moisture Sensor 

This device reads soil moisture as an analog value and transmits it to the internet via LoRa. Built with Pycom components and programmed in Micropython.

## Components:
* [LoPy 4](https://www.mouser.ca/ProductDetail/Pycom/LoPy-40?qs=sGAEpiMZZMve4%2FbfQkoj%252BPXa4DUIcH9VgIK4TTQpqCo%3D)
* [Expansion Board](https://www.mouser.ca/ProductDetail/Pycom/Expansion-Board-V3?qs=sGAEpiMZZMve4%2FbfQkoj%252BGKaEHSTRFNGwHs935CneW8%3D) OR [Pytrack](https://www.mouser.ca/ProductDetail/Pycom/Pytrack?qs=sGAEpiMZZMu3sxpa5v1qriV5vgGpNFXkgNIDo7yPdns%3D)
* [Analog Moisture Sensor](https://www.mouser.ca/ProductDetail/SparkFun/SEN-13322?qs=sGAEpiMZZMt6ebhnBMWiDNb7FPTjSkoEa2jLwS6OYSTZk%2FLOL3SNEw%3D%3D)
* [Pycom Universal IP67 Case](https://www.digikey.ca/product-detail/en/pycom-ltd/IP67-CASE-FOR-PYSENSE-PYTRACK/1871-1024-ND/9557027)
* [Pycom Sigfox/LoRa Antenna Kit](https://www.digikey.ca/product-detail/en/pycom-ltd/SIGFOX-LORA-ANTENNA-KIT/1871-1005-ND/7721843)
* [Solid Core Hookup Wire](https://www.amazon.ca/dp/B07926QP4J/ref=sspa_dk_detail_6?psc=1&pd_rd_i=B07926QP4J&pd_rd_w=zq671&pf_rd_p=4b7c8c1c-293f-4b1e-a49a-8787dff31bcb&pd_rd_wg=roMvl&pf_rd_r=114R3TJYPE5EXKADZG3B&pd_rd_r=61aeb009-6071-11e9-99af-1d04fb59fc70)
* [LiPo Battery with JST connector](https://www.adafruit.com/product/258)
* [Sugru](https://www.amazon.ca/Sugru-Mouldable-Glue-Family-Safe-Skin-Friendly/dp/B0763RG7FQ/ref=sr_1_1?hvadid=208253734020&hvdev=c&hvlocphy=9001365&hvnetw=g&hvpos=1t1&hvqmt=e&hvrand=16380141460298337848&hvtargid=kwd-296167437100&keywords=sugru&qid=1555437525&refinements=p_85%3A5690392011&rnid=5690384011&rps=1&s=gateway&sr=8-1)

## Setup:

### Hardware:

Before use, the firmware on the LoPy 4 and Expansion Board/ Pytrack must be updated to the current version. 

To update the firmware on the Expansion Board/Pytrack follow the instructions at the following [link](https://docs.pycom.io/pytrackpysense/installation/firmware.html)

Next, update the firmware on the LoPy 4 follow the instructions at the following [link](https://docs.pycom.io/gettingstarted/installation/firmwaretool.html)

### Programming Environment:

Pycom offers a plugin for Visual Studio Code called PyMakr which allows for easy development on Pycom devices.

Follow the instructions at the following [link](https://docs.pycom.io/pymakr/installation/vscode.html) to install PyMakr.

A Pycom microcontroller can be connected to in two ways, (1) via [USB](https://docs.pycom.io/pymakr/installation/vscode.html#connecting-via-serial-usb) and (2) via [Telnet](https://docs.pycom.io/pymakr/installation/vscode.html#connecting-via-telnet)

#### Using PyMakr:

Along the bottom of your VSCode Window with PyMakr installed, you will see the following toolbar.

![PyMakr Toolbar](https://docs.pycom.io/.gitbook/assets/vsc_config_step_1-1.png)

* **Run:** runs the code in the currently open file once, this code is not saved into flash memory
* **Upload:** Uploads ALL the code in the current workspace folder to flash memory and runs it. This code will run on the device automatically when it is turned on
* **Download:** downloads code from device to computer

#### Useful PyMakr Commands:

* `os.uname()`: shows current version of firmware
* `os.mkfs('/flash')`: erases flash memory

