<h1 align="center">
    <img width="600" src="header.png" align="center"></img>
</h1>
<p align="center">🖱️ Control mouse actions through keyboard interactions.</p>

<p align="center">
  <a aria-label="Node version" href="https://www.python.org/downloads/release/python-370/">
    <img src="https://img.shields.io/badge/python-3.7+-info?logo=Python"></img>
  </a>
</p>


## 🖱️ mouse-cli

<p align="left">
  <a target="_blank" href="https://mateusaquino.github.io/stardewids/"><img width="428px" alt="Example Overlay" title="Example Overlay" align="right" src="https://github.com/user-attachments/assets/75db6de8-aa28-4e6f-870b-88e2860d325f"/></a>
</p>

`mouse-cli` is a tool designed to enhance mouse accessibility by allowing users to interact with their mouse using keyboard shortcuts. It overlays the screen with a transparent grid or custom interface, enabling fast and precise mouse actions, such as clicking or dragging, using predefined keyboard inputs. This tool is particularly useful for users with limited mobility or those who prefer keyboard-based interaction.

### 🚀 Installation

#### Prerequisites

- Python 3.7 or higher
- Required Python packages:
  - `pyautogui`
  - `PyQt5`

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/MateusAquino/mouse-cli.git
   cd mouse-cli
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tool:
   ```bash
   python init.py
   ```

4. (optional) Create a shortcut to the script for easier access (e.g., on .zshrc):
   ```bash
   function mouse-cli { python /path/to/mouse-cli/init.py $@ }
   ```

You can now set up custom shortcuts for `mouse-cli` in your distro to suit your specific needs.

---

### ⌨️ Keyboard Shortcuts

- **Escape/Delete:** Exit the overlay.
- **Backspace:** Reset the active selection or exit if none is active.
- **Space:** Temporarily increase opacity to 100%.
- **Alphanumeric Keys (0-9, A-Z):** Navigate and select grid elements.

---

### 📟 Usage

The tool can be launched with various optional arguments to customize its behavior. Below is the list of available arguments:

```bash
usage: init.py [-h] [--exclude-numbers {none,all,x,y}] [--opacity OPACITY] [--view {grid,cartesian,cross}] [--one-by-one] [--color COLOR]
               [--active-color ACTIVE_COLOR] [--background-color BACKGROUND_COLOR] [--font FONT] [--size SIZE]
               [--button {left,right,middle,double,move,drag,scroll}] [--use-current-position] [--scroll-factor SCROLL_FACTOR]
```

#### Key Options

- **`--help` or `-h`:** Show the help message and exit.
- **`--exclude-numbers` or `-en`:** Exclude numbers from the grid (options: `none`, `all`, `x`, `y`).
- **`--opacity` or `-o`:** Set the overlay opacity (default: `0.45`).
- **`--view` or `-v`:** Set the view layout (`grid`, `cartesian`, or `cross`).
- **`--one-by-one` or `-obo`:** Enable single-step navigation.
- **`--color` or `-c`:** Set the primary grid color.
- **`--active-color` or `-ac`:** Set the active color.
- **`--background-color` or `-bc`:** Set the background color.
- **`--font` or `-f`:** Set the font family.
- **`--size` or `-s`:** Set the font size.
- **`--button` or `-b`:** Define the mouse action (e.g., `left`, `right`, `middle`, `double`, `drag`, `scroll`).
- **`--use-current-position` or `-p`:** Directly execute the mouse action at the current position.
- **`--scroll-factor` or `-sf`:** Set the scroll factor for the `scroll` action.

#### Example Commands

1. Launch the overlay with default settings:
   ```bash
   mouse-cli
   ```

2. Launch the overlay with custom colors, opacity and font family/size:
   ```bash
   mouse-cli -c "#FF00007F" -ac "#00FF007F" -bc "#000000FF" -o 0.6 -s 16 -f "Fira Code"
   ```

3. Use the tool for a drag action:
   ```bash
   mouse-cli -b move # Set start position
   mouse-cli -b drag # Drag to end position
   ```

4. Scroll the mouse wheel:
   ```bash
   mouse-cli -b scroll -sf 1 # Scroll up (selecting location)
   mouse-cli -b scroll -sf -1 # Scroll down (selecting location)
   mouse-cli -b scroll -sf 1 -p # Scroll up (from current location)
   mouse-cli -b scroll -sf -1 -p # Scroll down (from current location)
   ```

---

### 🤝 Contribution

We welcome contributions! Feel free to submit issues or pull requests on [GitHub](https://github.com/yourusername/mouse-keyboard-overlay).

#### To Contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Description of changes"`).
4. Push to your branch (`git push origin feature-name`).
5. Open a pull request.

---

### 🫂 Acknowledgments

- [**mouseless:**](https://mouseless.click/) For the inspiration.
- **PyQt5:** For the GUI framework.
- **pyautogui:** For mouse control automation.
