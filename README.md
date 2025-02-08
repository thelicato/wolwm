<!-- omit in toc -->
# wolwm

<div align="center" style="text-align:center">
  <br>
  <a href=""><img src="./logo.png" alt="wolwm Logo" width="200px;"></a>
  <br /><br/>
</div>

**WOLWM (Wake-on-LAN Web Manager)** is an easy-to-use web application that allows you to remotely wake up devices on your local network using **Wake-on-LAN (WoL) magic packets**. With a clean UI and simple configuration, WOLWM makes it effortless to bring your computers online from anywhere.

## 🎯 Features

- 🌐 **Web-based Interface** – No need for CLI commands; manage Wake-on-LAN from a browser.
- ⚡ **Send Magic Packets** – Wake up devices remotely with a single click.
- 📋 **Device Management** – Save and manage multiple devices for quick access.
- 🔄 **Logging & History** – Track which devices were woken up and when.

## 📌 Prerequisites

To use WOLWM, ensure you have:

- A device with **Wake-on-LAN** enabled in BIOS and OS.
- A **web server** to host the app (e.g., Node.js, Flask, or PHP-based servers).
- **Network access** to the target devices (they should be in the same subnet or properly routed).

## 📖 Wake-on-LAN Explained

Wake-on-LAN (WoL) is a networking standard that allows you to remotely wake up a powered-off computer using a **magic packet** sent over the network. The system must support WoL, and it must be enabled in both BIOS/UEFI and OS settings.

## 🛠️ Troubleshooting

- **Device not waking up?** Ensure WoL is enabled in BIOS and OS.
- **Magic packet not reaching the device?** Check firewall and network configurations.
- **Using a VPN?** Wake-on-LAN usually doesn’t work across different subnets without special routing.

## 🏗️ Future Improvements

- 🔄 Scheduled wake-ups & shutdowns.

## 📜 License

This project is licensed under the **MIT License**.

## ❤️ Contributing

Contributions are welcome! Feel free to open issues or submit pull requests on [GitHub](https://github.com/thelicato/wolwm).