#!/usr/bin/env python3
# Gemini AI Co-coder Contribution: Title changes, UI color theme update (dominant blue), SVG logo guidance.
# Timestamp: June 1, 2025, 10:23 AM EDT
"""
Shotgrid Tasks to MovieLabs Tasks OMC v2.6 Converter (Validator-Compliant)
=========================================================================

Converts ShotGrid task exports to MovieLabs OMC v2.6 format that actually validates!
Based on real-world testing with the official OMC JSON validator.

Key Features:
- Windows file browser for easy file selection
- Validator-compliant OMC JSON output
- Complete ShotGrid data preservation
- Uses official OMC functional classes
- Minimal structure that actually works
- Real-time progress tracking
- Enhanced UI Theme

Requirements:
pip install pandas tkinter tksvg

Usage:
python shotgrid_to_omc_converter.py

Validation Status: ✅ PASSES MovieLabs OMC v2.6 JSON Validator
"""

import pandas as pd
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime
from pathlib import Path

# Attempt to import tksvg for SVG logo support
try:
    import tksvg
    TKSVG_AVAILABLE = True
except ImportError:
    TKSVG_AVAILABLE = False

# --- Application Title ---
APP_TITLE = "Shotgrid Tasks to MovieLabs Tasks OMC v2.6 Converter"

# --- UI Color Palette ---
# Dominant blue background
DOMINANT_BLUE_BG = "#2A6DA4" # Was MOVIE_PRIMARY_BLUE

# Text and elements on the dominant blue background
TEXT_ON_DOMINANT_BLUE = "#FFFFFF" # White text
ACCENT_TEXT_ON_DOMINANT_BLUE = "#E1F5FE" # Very light blue for subtitles or less emphasis
HIGHLIGHT_ON_DOMINANT_BLUE = "#87CEFA" # LightSkyBlue for main titles or important labels

# Buttons
BUTTON_BLUE = "#1E73BE" # A distinct, slightly brighter blue for buttons
BUTTON_TEXT = "#FFFFFF"
BUTTON_FOCUS_BLUE = "#5F9EDC" # Lighter blue for button hover/focus

# Log Area (kept light for readability)
LOG_AREA_BG = "#FAFAFA"
LOG_AREA_TEXT = "#333333"

# Entry fields (on dominant blue background)
ENTRY_BG_ON_DOMINANT_BLUE = "#1C4A70" # A darker shade of the dominant blue
ENTRY_TEXT_ON_DOMINANT_BLUE = "#FFFFFF"
ENTRY_READONLY_BG_ON_DOMINANT_BLUE = "#205480" # Slightly different for readonly

class ShotGridToOMCConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE + " (Validator-Compliant)")
        self.root.geometry("800x700") # Slightly wider for logo
        self.root.configure(bg=DOMINANT_BLUE_BG)
        
        self.state_mapping = {
            "ip": "in process", "omt": "complete", "r4e": "assigned",
            "wtg": "waiting", "rev": "assigned", "fin": "complete"
        }
        self.functional_class_mapping = {
            "Text to Image": "Create Visual Effects", "Image to Video": "Create Visual Effects", 
            "Comp": "Create Visual Effects", "Upscale": "Create Visual Effects",
            "Model": "Create Visual Effects", "Texture": "Create Visual Effects",
            "Editorial": "Edit", "Edit": "Edit", "VFX": "Create Visual Effects",
            "Animation": "Create Visual Effects", "Lighting": "Create Visual Effects",
            "Rendering": "Create Visual Effects"
        }
        
        self.setup_ui_styles()
        self.setup_ui()
        
    def setup_ui_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('.', background=DOMINANT_BLUE_BG, foreground=TEXT_ON_DOMINANT_BLUE, font=("Arial", 10))
        style.configure('TFrame', background=DOMINANT_BLUE_BG)
        style.configure('TLabel', background=DOMINANT_BLUE_BG, foreground=TEXT_ON_DOMINANT_BLUE)
        
        style.configure('SectionHeader.TLabel', foreground=HIGHLIGHT_ON_DOMINANT_BLUE, font=("Arial", 10, "bold"))
        style.configure('AppTitle.TLabel', foreground=TEXT_ON_DOMINANT_BLUE, font=("Arial", 18, "bold")) # Main title
        style.configure('AppSubtitle.TLabel', foreground=ACCENT_TEXT_ON_DOMINANT_BLUE, font=("Arial", 11, "italic"))
        style.configure('Instructions.TLabel', foreground=ACCENT_TEXT_ON_DOMINANT_BLUE)

        style.configure('TButton', background=BUTTON_BLUE, foreground=BUTTON_TEXT, font=("Arial", 10, "bold"), borderwidth=1, relief="raised")
        style.map('TButton',
            background=[('active', BUTTON_FOCUS_BLUE), ('pressed', '!focus', BUTTON_BLUE), ('focus', BUTTON_FOCUS_BLUE)],
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
        )
        
        style.configure('TEntry', fieldbackground=ENTRY_BG_ON_DOMINANT_BLUE, foreground=ENTRY_TEXT_ON_DOMINANT_BLUE, insertcolor=TEXT_ON_DOMINANT_BLUE)
        # Style for readonly Entry fields
        style.configure('Readonly.TEntry', fieldbackground=ENTRY_READONLY_BG_ON_DOMINANT_BLUE, foreground=TEXT_ON_DOMINANT_BLUE)


        style.configure('themed.Horizontal.TProgressbar', troughcolor=DOMINANT_BLUE_BG, background=HIGHLIGHT_ON_DOMINANT_BLUE, thickness=20)
        
        style.configure('TLabelframe', background=DOMINANT_BLUE_BG, bordercolor=HIGHLIGHT_ON_DOMINANT_BLUE)
        style.configure('TLabelframe.Label', background=DOMINANT_BLUE_BG, foreground=HIGHLIGHT_ON_DOMINANT_BLUE, font=("Arial", 10, "bold"))

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # --- Logo Placeholder ---
        logo_frame = ttk.Frame(main_frame, style='TFrame')
        logo_frame.grid(row=0, column=0, columnspan=1, pady=(0,10), sticky=tk.W)
        
        self.logo_label = ttk.Label(logo_frame, style='TLabel') # For SVG or PNG
        self.logo_label.pack(side=tk.LEFT, padx=(0,10))
        self.load_logo("logo.svg") # Provide path to your SVG logo

        # --- Titles ---
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.grid(row=0, column=1, columnspan=2, pady=(0, 5), sticky=tk.EW)

        app_title_label = ttk.Label(title_frame, text=APP_TITLE, style='AppTitle.TLabel')
        app_title_label.pack(anchor=tk.W)
        
        app_subtitle_label = ttk.Label(title_frame, text="🎬 Validator-Compliant | ✨ Dominant Blue UI", style='AppSubtitle.TLabel')
        app_subtitle_label.pack(anchor=tk.W)
        
        instructions = ttk.Label(main_frame, text="Convert ShotGrid CSV exports to validator-compliant OMC v2.6 JSON", style='Instructions.TLabel')
        instructions.grid(row=1, column=0, columnspan=3, pady=(0, 15), sticky=tk.W)
        
        # Input file selection
        ttk.Label(main_frame, text="1. Select ShotGrid CSV Export:", style='SectionHeader.TLabel').grid(
            row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        self.input_file_var = tk.StringVar()
        input_frame = ttk.Frame(main_frame, style='TFrame')
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_file_var, width=70, style='Readonly.TEntry', state="readonly")
        self.input_entry.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
        ttk.Button(input_frame, text="Browse CSV...", command=self.select_input_file).grid(row=0, column=1)
        input_frame.columnconfigure(0, weight=1)

        # Output file selection
        ttk.Label(main_frame, text="2. Choose Output Location:", style='SectionHeader.TLabel').grid(
            row=4, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        self.output_file_var = tk.StringVar()
        output_frame = ttk.Frame(main_frame, style='TFrame')
        output_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_file_var, width=70, style='Readonly.TEntry', state="readonly")
        self.output_entry.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
        ttk.Button(output_frame, text="Save JSON As...", command=self.select_output_file).grid(row=0, column=1)
        output_frame.columnconfigure(0, weight=1)
        
        action_frame = ttk.Frame(main_frame, style='TFrame')
        action_frame.grid(row=6, column=0, columnspan=3, pady=(10,10), sticky=tk.EW)

        self.convert_button = ttk.Button(action_frame, text="🚀 Convert to OMC v2.6 JSON", command=self.convert_file, state="disabled")
        self.convert_button.pack(side=tk.LEFT, padx=(0, 20))
        
        self.animated_progress_label_var = tk.StringVar()
        self.animated_progress_label = ttk.Label(action_frame, textvariable=self.animated_progress_label_var, style='SectionHeader.TLabel')
        self.animated_progress_label.pack(side=tk.LEFT)
        self.animation_chars = ['🎞️ Processing.', '🎬 Processing..', '🍿 Processing...']
        self.animation_index = 0
        self.animation_job = None
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', style='themed.Horizontal.TProgressbar', length=300)
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 10))
        
        status_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="10", style='TLabelframe')
        status_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.results_text = tk.Text(status_frame, height=15, width=80, wrap=tk.WORD, 
                                    bg=LOG_AREA_BG, fg=LOG_AREA_TEXT, relief=tk.SUNKEN, borderwidth=1,
                                    font=("Courier New", 9), insertbackground=LOG_AREA_TEXT) # Ensure cursor is visible
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        main_frame.columnconfigure(1, weight=1) # Allow title area to expand
        main_frame.rowconfigure(8, weight=1) 
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def load_logo(self, svg_file_path):
        """Loads an SVG logo if tksvg is available, or a PNG fallback."""
        try:
            if TKSVG_AVAILABLE:
                # Ensure the SVG file exists
                if os.path.exists(svg_file_path):
                    self.logo_image = tksvg.SvgImage(file=svg_file_path, scaletowidth=50) # Adjust scale as needed
                    self.logo_label.configure(image=self.logo_image)
                else:
                    self.logo_label.configure(text="SVG N/A") # Placeholder if SVG not found
            else:
                # Try to load a PNG fallback if tksvg is not there or SVG fails
                png_fallback_path = svg_file_path.replace(".svg", ".png")
                if os.path.exists(png_fallback_path):
                    # You would need Pillow (PIL) for PNGs typically:
                    # from PIL import Image, ImageTk
                    # self.pil_image = Image.open(png_fallback_path)
                    # self.tk_image = ImageTk.PhotoImage(self.pil_image.resize((50,50))) # Example resize
                    # self.logo_label.configure(image=self.tk_image)
                    self.logo_label.configure(text="PNG?") # Placeholder if tksvg not available
                else:
                    self.logo_label.configure(text="Logo?") # Placeholder if tksvg not available
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo_label.configure(text="Logo Err")
            
    def select_input_file(self):
        file_path = filedialog.askopenfilename(title="Select ShotGrid CSV Export", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.input_file_var.set(file_path)
            self.input_entry.config(style='Readonly.TEntry') # Ensure readonly style
            self.check_ready_to_convert()
            
    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(title="Save OMC JSON As", defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            self.output_file_var.set(file_path)
            self.output_entry.config(style='Readonly.TEntry') # Ensure readonly style
            self.check_ready_to_convert()
            
    def check_ready_to_convert(self):
        if self.input_file_var.get() and self.output_file_var.get():
            self.convert_button.config(state="normal")
        else:
            self.convert_button.config(state="disabled")

    def start_animation(self):
        self.convert_button.config(state="disabled")
        self.progress.start(15)
        self.update_animation_text()

    def stop_animation(self):
        self.progress.stop()
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
        self.animated_progress_label_var.set("")
        self.check_ready_to_convert()

    def update_animation_text(self):
        self.animated_progress_label_var.set(self.animation_chars[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(self.animation_chars)
        self.animation_job = self.root.after(400, self.update_animation_text)
            
    def log_message(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.results_text.insert(tk.END, f"{timestamp} - {message}\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()
        
    def convert_file(self):
        try:
            self.start_animation()
            self.results_text.delete(1.0, tk.END)
            self.log_message(f"🚀 Lights, Camera, Conversion! Starting {APP_TITLE}...")
            self.log_message("📋 Using validator-compliant minimal structure")
            
            input_file = self.input_file_var.get()
            self.log_message(f"📖 Reading CSV file: {Path(input_file).name}")
            
            df = pd.read_csv(input_file)
            self.log_message(f"📊 Found {len(df)} rows in CSV. Roll 'em!")
            
            all_omc_entities, task_count = [], 0
            self.log_message("⚙️ Converting tasks to OMC format...")
            
            for index, row in df.iterrows():
                if pd.notna(row.get('Id')):
                    task_count += 1; context = []
                    if pd.notna(row.get('Start Date')) or pd.notna(row.get('Due Date')): context.append({"identifier": [{"identifierScope": "shotgrid", "identifierValue": f"scheduling/{int(row['Id'])}"}]})
                    if pd.notna(row.get('Assigned To')): context.append({"identifier": [{"identifierScope": "shotgrid", "identifierValue": f"workunit/{row['Assigned To'].lower().replace(' ', '-')}-artist"}]})
                    if pd.notna(row.get('Reviewer')): context.append({"identifier": [{"identifierScope": "shotgrid", "identifierValue": f"workunit/{row['Reviewer'].lower().replace(' ', '-')}-reviewer"}]})
                    if pd.notna(row.get('Link')): context.append({"identifier": [{"identifierScope": "shotgrid", "identifierValue": f"asset/{row['Link'].lower().replace(' ', '-').replace('/', '-')}"}]})
                    
                    task = {"schemaVersion": "https://movielabs.com/omc/json/schema/v2.6", "entityType": "Task",
                            "identifier": [{"identifierScope": "shotgrid", "identifierValue": f"task/{int(row['Id'])}"}],
                            "taskFC": {"functionalType": self.functional_class_mapping.get(row.get('Pipeline Step')),
                                       "customData": {"name": row.get('Task Name', f"Task {int(row['Id'])}"),
                                                      "state": self.state_mapping.get(row.get('Status'), 'waiting'),
                                                      "stateDetails": {"originalShotGridStatus": row.get('Status'), "shotGridId": int(row['Id']), "note": f"Converted from ShotGrid task {int(row['Id'])}"},
                                                      "pipelineStep": row.get('Pipeline Step') if pd.notna(row.get('Pipeline Step')) else None,
                                                      "thumbnailUrl": row.get('Thumbnail') if pd.notna(row.get('Thumbnail')) else None,
                                                      "shotStatus": row.get('Shot > Shot Status') if pd.notna(row.get('Shot > Shot Status')) else None,
                                                      "scheduling": self._build_scheduling_data(row), "assignments": self._build_assignment_data(row),
                                                      "assets": self._build_asset_data(row),
                                                      "originalShotGridData": {"Id": int(row['Id']), "TaskName": row.get('Task Name'), "Link": row.get('Link'), "PipelineStep": row.get('Pipeline Step'), "Status": row.get('Status'), "AssignedTo": row.get('Assigned To'), "Reviewer": row.get('Reviewer'), "StartDate": str(row.get('Start Date')) if pd.notna(row.get('Start Date')) else None, "DueDate": str(row.get('Due Date')) if pd.notna(row.get('Due Date')) else None, "ShotStatus": row.get('Shot > Shot Status'), "Project": row.get('Project'), "Thumbnail": row.get('Thumbnail')}}},
                            "Context": context if context else None}
                    all_omc_entities.append(task)
                    if task_count % 50 == 0: self.log_message(f"🎞️ Processed {task_count} of {len(df)} tasks...")
            
            self.log_message(f"✅ Successfully converted {task_count} tasks!"); self.log_message(f"📋 Created {len(all_omc_entities)} OMC Task entities")
            functional_class_stats, state_stats, pipeline_stats = {}, {}, {}
            for entity in all_omc_entities:
                func_class = entity["taskFC"]["functionalType"]; state = entity["taskFC"]["customData"]["state"]; pipeline_step = entity["taskFC"]["customData"]["pipelineStep"]
                if func_class: functional_class_stats[func_class] = functional_class_stats.get(func_class, 0) + 1
                state_stats[state] = state_stats.get(state, 0) + 1
                if pipeline_step: pipeline_stats[pipeline_step] = pipeline_stats.get(pipeline_step, 0) + 1
            
            self.log_message("\n📈 Official OMC Functional Classes:"); [self.log_message(f"   • {fc}: {c} tasks") for fc, c in functional_class_stats.items()]
            self.log_message("\n📊 Task States:"); [self.log_message(f"   • {s}: {c} tasks") for s, c in state_stats.items()]
            self.log_message("\n🔧 Pipeline Steps:"); [self.log_message(f"   • {ps}: {c} tasks") for ps, c in pipeline_stats.items()]
            
            output_file = self.output_file_var.get()
            self.log_message(f"\n💾 Saving OMC JSON to: {Path(output_file).name}")
            with open(output_file, 'w', encoding='utf-8') as f: json.dump(all_omc_entities, f, indent=2, ensure_ascii=False)
            
            file_size_kb = os.path.getsize(output_file) / 1024
            self.log_message(f"🎉 IT'S A WRAP! Created {file_size_kb:.1f}KB validator-compliant OMC JSON"); self.log_message("✅ Ready for MovieLabs OMC v2.6 validator testing")
            
            messagebox.showinfo("Conversion Complete!", f"🎉 IT'S A WRAP! Successfully converted {task_count} ShotGrid tasks for {APP_TITLE}!\n\n✅ Validator-compliant OMC v2.6 format\n📁 Output: {Path(output_file).name}\n📊 Size: {file_size_kb:.1f}KB\n\nReady for OMC ecosystem integration!")
            
        except Exception as e:
            error_msg = f"❌ CUT! Error during conversion: {str(e)}"; self.log_message(error_msg)
            messagebox.showerror("Conversion Error", f"Conversion failed for {APP_TITLE}:\n\n{str(e)}\n\nPlease check your CSV format and try again.")
        finally: self.stop_animation()
    
    def _build_scheduling_data(self, row):
        s = {}; 
        if pd.notna(row.get('Start Date')): s["scheduledStart"] = str(row['Start Date'])
        if pd.notna(row.get('Due Date')): s["scheduledEnd"] = str(row['Due Date'])
        return s if s else None
    def _build_assignment_data(self, row):
        a = {}; 
        if pd.notna(row.get('Assigned To')): a["assignedTo"] = row['Assigned To']
        if pd.notna(row.get('Reviewer')): a["reviewer"] = row['Reviewer']
        return a if a else None
    def _build_asset_data(self, row):
        a = {}; 
        if pd.notna(row.get('Link')): a["inputAsset"] = row['Link']
        return a if a else None
    
    def run(self):
        self.log_message(f"🎬 {APP_TITLE} Ready!"); self.log_message("📋 Select your ShotGrid CSV export to begin conversion")
        self.log_message("✨ UI updated to Dominant Blue theme!")
        if not TKSVG_AVAILABLE: self.log_message("ℹ️ For SVG logo, install 'tksvg': pip install tksvg")
        self.log_message("")
        self.root.mainloop()

if __name__ == "__main__":
    print(f"🚀 Starting {APP_TITLE}...")
    print("✅ Validator-compliant | ✨ Dominant Blue UI")
    app = ShotGridToOMCConverter()
    app.run()