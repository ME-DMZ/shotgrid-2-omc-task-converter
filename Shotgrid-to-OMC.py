#!/usr/bin/env python3
# Gemini AI Co-coder Contribution: Refined success definition for online validator (passed/generated).
# Timestamp: June 1, 2025, 1:46 PM EDT
"""
Shotgrid Tasks to MovieLabs Tasks OMC v2.6 Converter (Validator-Compliant)
=========================================================================

Converts ShotGrid task exports to MovieLabs OMC v2.6 format. Includes online
validation against the official MovieLabs OMC validator using the /api/check endpoint.

Key Features:
- Windows file browser for easy file selection
- Validator-compliant OMC JSON output
- Complete ShotGrid data preservation
- Uses official OMC functional classes
- Minimal structure that actually works
- Real-time progress tracking
- Enhanced UI Theme
- Integrated Online OMC Validation

Requirements:
pip install pandas tkinter tksvg requests

Usage:
python shotgrid_to_omc_converter.py
"""

import pandas as pd
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime
from pathlib import Path
import requests # For online validation
import traceback # For detailed error logging

# Attempt to import tksvg for SVG logo support
try:
    import tksvg
    TKSVG_AVAILABLE = True
except ImportError:
    TKSVG_AVAILABLE = False

# --- Application Title ---
APP_TITLE = "Shotgrid Tasks to MovieLabs Tasks OMC v2.6 Converter"

# --- UI Color Palette (Dominant Blue Theme) ---
DOMINANT_BLUE_BG = "#2A6DA4"
TEXT_ON_DOMINANT_BLUE = "#FFFFFF"
ACCENT_TEXT_ON_DOMINANT_BLUE = "#E1F5FE"
HIGHLIGHT_ON_DOMINANT_BLUE = "#87CEFA" 
BUTTON_BLUE = "#1E73BE" 
BUTTON_TEXT = "#FFFFFF"
BUTTON_FOCUS_BLUE = "#5F9EDC" 
LOG_AREA_BG = "#FAFAFA"
LOG_AREA_TEXT = "#333333"
ENTRY_BG_ON_DOMINANT_BLUE = "#1C4A70" 
ENTRY_TEXT_ON_DOMINANT_BLUE = "#FFFFFF"
ENTRY_READONLY_BG_ON_DOMINANT_BLUE = "#205480"

# --- Online Validator ---
VALIDATOR_API_URL = "https://omc-validator.mc.movielabs.com/api/check"

class ShotGridToOMCConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE + " (Validator-Compliant)")
        self.root.geometry("800x750") 
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
        
        self.generated_json_path = None
        self.setup_ui_styles()
        self.setup_ui()
        
    def setup_ui_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background=DOMINANT_BLUE_BG, foreground=TEXT_ON_DOMINANT_BLUE, font=("Arial", 10))
        style.configure('TFrame', background=DOMINANT_BLUE_BG)
        style.configure('TLabel', background=DOMINANT_BLUE_BG, foreground=TEXT_ON_DOMINANT_BLUE)
        style.configure('SectionHeader.TLabel', foreground=HIGHLIGHT_ON_DOMINANT_BLUE, font=("Arial", 10, "bold"))
        style.configure('AppTitle.TLabel', foreground=TEXT_ON_DOMINANT_BLUE, font=("Arial", 18, "bold"))
        style.configure('AppSubtitle.TLabel', foreground=ACCENT_TEXT_ON_DOMINANT_BLUE, font=("Arial", 11, "italic"))
        style.configure('Instructions.TLabel', foreground=ACCENT_TEXT_ON_DOMINANT_BLUE)
        style.configure('TButton', background=BUTTON_BLUE, foreground=BUTTON_TEXT, font=("Arial", 10, "bold"), borderwidth=1, relief="raised")
        style.map('TButton',
            background=[('active', BUTTON_FOCUS_BLUE), ('pressed', '!focus', BUTTON_BLUE), ('focus', BUTTON_FOCUS_BLUE)],
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
        )
        style.configure('TEntry', fieldbackground=ENTRY_BG_ON_DOMINANT_BLUE, foreground=ENTRY_TEXT_ON_DOMINANT_BLUE, insertcolor=TEXT_ON_DOMINANT_BLUE)
        style.configure('Readonly.TEntry', fieldbackground=ENTRY_READONLY_BG_ON_DOMINANT_BLUE, foreground=TEXT_ON_DOMINANT_BLUE)
        style.configure('themed.Horizontal.TProgressbar', troughcolor=DOMINANT_BLUE_BG, background=HIGHLIGHT_ON_DOMINANT_BLUE, thickness=20)
        style.configure('TLabelframe', background=DOMINANT_BLUE_BG, bordercolor=HIGHLIGHT_ON_DOMINANT_BLUE)
        style.configure('TLabelframe.Label', background=DOMINANT_BLUE_BG, foreground=HIGHLIGHT_ON_DOMINANT_BLUE, font=("Arial", 10, "bold"))

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.grid(row=0, column=0, columnspan=3, sticky=tk.EW, pady=(0,10))
        self.logo_label = ttk.Label(header_frame, style='TLabel')
        self.logo_label.pack(side=tk.LEFT, padx=(0,20), anchor=tk.NW)
        self.load_logo("logo.svg") 
        title_subtitle_frame = ttk.Frame(header_frame, style='TFrame')
        title_subtitle_frame.pack(side=tk.LEFT, anchor=tk.NW)
        app_title_label = ttk.Label(title_subtitle_frame, text=APP_TITLE, style='AppTitle.TLabel')
        app_title_label.pack(anchor=tk.W)
        app_subtitle_label = ttk.Label(title_subtitle_frame, text="🎬 Validator-Compliant | ✨ Online Validation", style='AppSubtitle.TLabel')
        app_subtitle_label.pack(anchor=tk.W)
        
        instructions = ttk.Label(main_frame, text="Convert ShotGrid CSV to OMC JSON, then validate online.", style='Instructions.TLabel')
        instructions.grid(row=1, column=0, columnspan=3, pady=(0, 15), sticky=tk.W)
        
        ttk.Label(main_frame, text="1. Select ShotGrid CSV Export:", style='SectionHeader.TLabel').grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        self.input_file_var = tk.StringVar()
        input_frame = ttk.Frame(main_frame, style='TFrame'); input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_file_var, width=70, style='Readonly.TEntry', state="readonly")
        self.input_entry.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
        ttk.Button(input_frame, text="Browse CSV...", command=self.select_input_file).grid(row=0, column=1)
        input_frame.columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="2. Choose Output Location:", style='SectionHeader.TLabel').grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        self.output_file_var = tk.StringVar()
        output_frame = ttk.Frame(main_frame, style='TFrame'); output_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_file_var, width=70, style='Readonly.TEntry', state="readonly")
        self.output_entry.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
        ttk.Button(output_frame, text="Save JSON As...", command=self.select_output_file).grid(row=0, column=1)
        output_frame.columnconfigure(0, weight=1)
        
        action_buttons_frame = ttk.Frame(main_frame, style='TFrame')
        action_buttons_frame.grid(row=6, column=0, columnspan=3, pady=(10,0), sticky=tk.EW)
        self.convert_button = ttk.Button(action_buttons_frame, text="🚀 Convert to OMC JSON", command=self.convert_file, state="disabled")
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        self.validate_button = ttk.Button(action_buttons_frame, text="🔎 Validate Online", command=self.validate_online, state="disabled")
        self.validate_button.pack(side=tk.LEFT, padx=(0, 20))
        self.animated_progress_label_var = tk.StringVar()
        self.animated_progress_label = ttk.Label(action_buttons_frame, textvariable=self.animated_progress_label_var, style='SectionHeader.TLabel')
        self.animated_progress_label.pack(side=tk.LEFT)
        self.animation_chars = ['🎞️ Processing.', '🎬 Processing..', '🍿 Processing...']
        self.animation_index = 0; self.animation_job = None
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', style='themed.Horizontal.TProgressbar', length=300)
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 10))
        
        status_frame = ttk.LabelFrame(main_frame, text="Conversion & Validation Log", padding="10", style='TLabelframe')
        status_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.results_text = tk.Text(status_frame, height=15, width=80, wrap=tk.WORD, bg=LOG_AREA_BG, fg=LOG_AREA_TEXT, relief=tk.SUNKEN, borderwidth=1, font=("Courier New", 9), insertbackground=LOG_AREA_TEXT)
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)); scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        main_frame.columnconfigure(0, weight=1); main_frame.rowconfigure(8, weight=1) 
        status_frame.columnconfigure(0, weight=1); status_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1); self.root.rowconfigure(0, weight=1)

    def load_logo(self, relative_logo_path):
        try:
            script_dir = Path(__file__).resolve().parent
            logo_path = script_dir / relative_logo_path
            if TKSVG_AVAILABLE and logo_path.is_file():
                self.logo_image = tksvg.SvgImage(file=str(logo_path), scaletowidth=40)
                self.logo_label.configure(image=self.logo_image)
            elif logo_path.is_file(): 
                 self.logo_label.configure(text="SVG")
            else: self.logo_label.configure(text="Logo N/A")
        except Exception as e:
            print(f"Error loading logo: {e}"); self.logo_label.configure(text="Logo Err")
            
    def select_input_file(self):
        fp = filedialog.askopenfilename(title="Select SG CSV", filetypes=[("CSV", "*.csv"), ("All", "*.*")])
        if fp: self.input_file_var.set(fp); self.input_entry.config(style='Readonly.TEntry'); self.check_ready_to_convert()
            
    def select_output_file(self):
        fp = filedialog.asksaveasfilename(title="Save OMC JSON", defaultextension=".json", filetypes=[("JSON", "*.json"), ("All", "*.*")])
        if fp: self.output_file_var.set(fp); self.output_entry.config(style='Readonly.TEntry'); self.check_ready_to_convert()
            
    def check_ready_to_convert(self):
        can_convert = bool(self.input_file_var.get() and self.output_file_var.get())
        self.convert_button.config(state="normal" if can_convert else "disabled")

    def start_animation(self, process_name="Processing"):
        self.convert_button.config(state="disabled"); self.validate_button.config(state="disabled")
        self.animation_chars = [f'🎞️ {process_name}.', f'🎬 {process_name}..', f'🍿 {process_name}...']
        self.progress.start(15); self.update_animation_text()

    def stop_animation(self):
        self.progress.stop()
        if self.animation_job: self.root.after_cancel(self.animation_job); self.animation_job = None
        self.animated_progress_label_var.set("")
        self.check_ready_to_convert()
        if self.generated_json_path and os.path.exists(self.generated_json_path):
             self.validate_button.config(state="normal")

    def update_animation_text(self):
        self.animated_progress_label_var.set(self.animation_chars[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(self.animation_chars)
        self.animation_job = self.root.after(400, self.update_animation_text)
            
    def log_message(self, message, clear_previous=False):
        if clear_previous: self.results_text.delete(1.0, tk.END)
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.results_text.insert(tk.END, f"{timestamp} - {message}\n")
        self.results_text.see(tk.END); self.root.update_idletasks()
        
    def convert_file(self): 
        self.generated_json_path = None 
        self.validate_button.config(state="disabled")
        try:
            self.start_animation("Converting")
            self.log_message(f"🚀 Lights, Camera, Conversion! Starting {APP_TITLE}...", clear_previous=True)
            input_file = self.input_file_var.get(); output_file = self.output_file_var.get()
            self.log_message(f"📖 Reading CSV file: {Path(input_file).name}")
            df = pd.read_csv(input_file); self.log_message(f"📊 Found {len(df)} rows. Roll 'em!")
            all_omc_entities, task_count = [], 0
            self.log_message("⚙️ Converting tasks to OMC format...")
            for index, row in df.iterrows():
                if pd.notna(row.get('Id')):
                    task_count += 1; context = []
                    if pd.notna(row.get('Start Date')) or pd.notna(row.get('Due Date')): context.append({"identifier": [{"identifierScope": "shotgrid", "identifierValue": f"scheduling/{int(row['Id'])}"}]})
                    if pd.notna(row.get('Assigned To')): context.append({"identifier": [{"identifierScope": "shotgrid", "identifierValue": f"workunit/{row['Assigned To'].lower().replace(' ', '-')}-artist"}]})
                    if pd.notna(row.get('Reviewer')): context.append({"identifier": [{"identifierScope": "shotgrid", "identifierValue": f"workunit/{row['Reviewer'].lower().replace(' ', '-')}-reviewer"}]})
                    if pd.notna(row.get('Link')): context.append({"identifier": [{"identifierScope": "shotgrid", "identifierValue": f"asset/{row['Link'].lower().replace(' ', '-').replace('/', '-')}"}]})
                    
                    original_sg_data_dict = {
                        "Id": int(row['Id']) if pd.notna(row.get('Id')) else None,
                        "TaskName": row.get('Task Name'), "Link": row.get('Link'),
                        "PipelineStep": row.get('Pipeline Step'), "Status": row.get('Status'),
                        "AssignedTo": row.get('Assigned To'), "Reviewer": row.get('Reviewer'),
                        "StartDate": str(row.get('Start Date')) if pd.notna(row.get('Start Date')) else None,
                        "DueDate": str(row.get('Due Date')) if pd.notna(row.get('Due Date')) else None,
                        "ShotStatus": row.get('Shot > Shot Status'), "Project": row.get('Project'),
                        "Thumbnail": row.get('Thumbnail')
                    }
                    original_sg_data_dict = {k: v for k, v in original_sg_data_dict.items() if v is not None}

                    task = {"schemaVersion": "https://movielabs.com/omc/json/schema/v2.6", 
                            "entityType": "Task", 
                            "identifier": [{"identifierScope": "shotgrid", "identifierValue": f"task/{int(row['Id'])}"}],
                            "taskFC": {"functionalType": self.functional_class_mapping.get(row.get('Pipeline Step')), 
                                       "customData": {"name": row.get('Task Name', f"Task {int(row['Id'])}"), 
                                                      "state": self.state_mapping.get(row.get('Status'), 'waiting'), 
                                                      "stateDetails": {"originalShotGridStatus": row.get('Status'), "shotGridId": int(row['Id']) if pd.notna(row.get('Id')) else None, "note": f"Converted from SG task {int(row['Id']) if pd.notna(row.get('Id')) else 'N/A'}"}, 
                                                      "pipelineStep": row.get('Pipeline Step') if pd.notna(row.get('Pipeline Step')) else None, 
                                                      "thumbnailUrl": row.get('Thumbnail') if pd.notna(row.get('Thumbnail')) else None, 
                                                      "shotStatus": row.get('Shot > Shot Status') if pd.notna(row.get('Shot > Shot Status')) else None, 
                                                      "scheduling": self._build_scheduling_data(row), 
                                                      "assignments": self._build_assignment_data(row), 
                                                      "assets": self._build_asset_data(row), 
                                                      "shotgridPassThroughData_json": json.dumps(original_sg_data_dict) if original_sg_data_dict else None
                                                     }
                                      },
                            "Context": context if context else None}
                    task = {k: v for k, v in task.items() if v is not None}
                    if task.get("taskFC") and task["taskFC"].get("customData"):
                         task["taskFC"]["customData"] = {k:v for k,v in task["taskFC"]["customData"].items() if v is not None}
                    if task.get("taskFC"):
                         task["taskFC"] = {k:v for k,v in task["taskFC"].items() if v is not None}

                    all_omc_entities.append(task)
                    if task_count % 50 == 0: self.log_message(f"🎞️ Processed {task_count} of {len(df)} tasks...")
            self.log_message(f"✅ Converted {task_count} tasks! {len(all_omc_entities)} OMC entities.")
            self.log_message(f"\n💾 Saving OMC JSON to: {Path(output_file).name}")
            with open(output_file, 'w', encoding='utf-8') as f: json.dump(all_omc_entities, f, indent=2, ensure_ascii=False)
            self.generated_json_path = output_file
            file_size_kb = os.path.getsize(output_file) / 1024
            self.log_message(f"🎉 IT'S A WRAP! Created {file_size_kb:.1f}KB OMC JSON. Ready for validation!")
            messagebox.showinfo("Conversion Complete!", f"🎉 Converted {task_count} tasks!\nOutput: {Path(output_file).name}\n\nReady to Validate Online!")
        except Exception as e:
            error_msg = f"❌ CUT! Conversion Error: {type(e).__name__} - {str(e)}"; self.log_message(error_msg)
            self.log_message(traceback.format_exc())
            messagebox.showerror("Conversion Error", f"Failed: {str(e)}\nCheck CSV & try again.")
        finally: self.stop_animation()

    def validate_online(self):
        if not self.generated_json_path or not os.path.exists(self.generated_json_path):
            messagebox.showerror("Validation Error", "No JSON file generated or found. Please convert first.")
            return

        self.log_message(f"\n🔎 Preparing to validate {Path(self.generated_json_path).name} online using {VALIDATOR_API_URL}...", clear_previous=False)
        self.start_animation("Validating")

        try:
            file_name_for_form = Path(self.generated_json_path).name
            with open(self.generated_json_path, 'rb') as f: 
                files_payload = {'file': (file_name_for_form, f, 'application/json')}
                self.log_message(f"📡 Sending data to MovieLabs Validator: {VALIDATOR_API_URL}")
                response = requests.post(VALIDATOR_API_URL, files=files_payload, timeout=45) 
            
            self.log_message(f"🛰️ Response received: HTTP {response.status_code}")
            response.raise_for_status() 
            validation_result = response.json()
            summary = validation_result.get("summary", {})
            details = validation_result.get("details", {})
            issues_by_rule = details.get("issues", {})
            
            # --- Refined Pass/Fail Logic based on user request ---
            has_critical_failure = False
            all_passed_or_generated = True # Assume true until a contradicting status is found
            
            if summary:
                for rule_id, status_val in summary.items():
                    status_val_lower = status_val.lower() # Case-insensitive check
                    if status_val_lower == "failed":
                        has_critical_failure = True
                        all_passed_or_generated = False # A failure means it's not this kind of success
                        break 
                    if status_val_lower not in ["passed", "generated"]:
                        all_passed_or_generated = False 
            elif issues_by_rule: 
                has_critical_failure = True 
                all_passed_or_generated = False
            elif not summary and not issues_by_rule: 
                 has_critical_failure = False 
                 all_passed_or_generated = False # Ambiguous, not the specific "passed or generated" success

            # Detailed logging of summary and issues
            self.log_message("\n📋 Validation Report:")
            if summary:
                self.log_message("  Summary by Rule:")
                for rule_id, status in sorted(summary.items()): self.log_message(f"    - {rule_id}: {status.upper()}")
            else: self.log_message("  No overall summary provided in response.")

            total_issues_logged = 0; issue_log_for_messagebox = []
            if issues_by_rule:
                self.log_message("  Detailed Issues by Rule:")
                for rule_id, issue_list in sorted(issues_by_rule.items()):
                    self.log_message(f"    Rule: {rule_id} ({len(issue_list)} issues)")
                    for i, issue_detail in enumerate(issue_list):
                        total_issues_logged +=1
                        issue_text = issue_detail.get("issue", "No issue text.")
                        exception_text = issue_detail.get("exception", "")
                        specifics_text = issue_detail.get("specifics", "")
                        context_type = issue_detail.get("context", {}).get("type", "N/A")
                        context_pointers = issue_detail.get("context", {}).get("jsonPointers", [])
                        log_entry = f"      [{i+1}] {issue_text} (Ctx: {context_type}, Ptrs: {context_pointers}"
                        if exception_text: log_entry += f", Exc: {exception_text}"
                        if specifics_text: log_entry += f", Specifics: {specifics_text}"
                        log_entry += ")"
                        self.log_message(log_entry)
                        if len(issue_log_for_messagebox) < 7: issue_log_for_messagebox.append(f"- {rule_id}: {issue_text[:120]}...")
            else: self.log_message("  No specific issues detailed in response.")
            self.log_message("-" * 50)

            # Final user messaging based on refined logic
            if has_critical_failure:
                self.log_message("❌ OVERALL VALIDATION: FAILED (due to one or more 'failed' rules).")
                failed_rules_summary_text = [f"- {rule}: FAILED" for rule, status in summary.items() if status.lower() == "failed"]
                messagebox.showerror("Validation Result: FAILED", 
                                     f"Validation FAILED.\n{total_issues_logged} issues reported (see log).\n\nFailed Rules:\n" + "\n".join(failed_rules_summary_text[:5]))
            elif all_passed_or_generated and summary : # Check 'summary' to ensure we have data for this conclusion
                self.log_message("✅ OVERALL VALIDATION: SUCCESSFUL (All rules reported as 'passed' or 'generated').")
                messagebox.showinfo("Validation Result: SUCCESSFUL", 
                                    "Validation Successful!\n\nAll checks have either 'passed' or were 'generated' by the validator (e.g., some identifiers). Your OMC JSON is considered compliant based on these results. Please review the log for full details.")
            elif not summary and not issues_by_rule:
                 self.log_message("❔ OVERALL VALIDATION: AMBIGUOUS (Validator response received, but no summary or issues provided).")
                 messagebox.showinfo("Validation Result: AMBIGUOUS", "Validator response received, but no summary or issues provided. Please review the log for the raw response if available.")
            else: # No "failed", but not exclusively "passed" or "generated"
                self.log_message("⚠️ OVERALL VALIDATION: PASSED (with other notes/statuses). Please review the log.")
                other_statuses_text = [f"- {rule}: {status.upper()}" for rule, status in summary.items() if status.lower() not in ["passed", "generated", "failed"]]
                message_detail = "JSON is valid (no rules failed).\nHowever, some rules have other statuses (e.g., warnings or unexpected results):\n" + "\n".join(other_statuses_text[:3]) + "\n\nReview log for full details."
                messagebox.showinfo("Validation Result: PASSED (with notes)", message_detail)

        except requests.exceptions.Timeout:
            self.log_message("❌ NETWORK ERROR: Validation request timed out.")
            messagebox.showerror("Validation Error", "Request to online validator timed out.")
        except requests.exceptions.HTTPError as e:
            self.log_message(f"❌ API ERROR: HTTP {e.response.status_code} - {e.response.reason}")
            try: err_details = e.response.json(); self.log_message(f"   Error details: {json.dumps(err_details, indent=2)}")
            except json.JSONDecodeError: self.log_message(f"   Error details: {e.response.text}")
            messagebox.showerror("Validation Error", f"API Error: {e.response.status_code}. Check log.")
        except requests.exceptions.RequestException as e:
            self.log_message(f"❌ VALIDATION ERROR: Could not connect/send: {e}")
            messagebox.showerror("Validation Error", f"Could not connect: {e}")
        except json.JSONDecodeError: 
            self.log_message("❌ ERROR: Could not decode validator's JSON response.")
            if 'response' in locals() and response and response.text: self.log_message(f"Raw response: {response.text[:1000]}...")
            messagebox.showerror("Validation Error", "Invalid JSON response from validator. Check log.")
        except Exception as e:
            self.log_message(f"❌ UNEXPECTED ERROR during validation: {type(e).__name__} - {e}")
            self.log_message(traceback.format_exc()) 
            messagebox.showerror("Validation Error", f"An unexpected error occurred: {e}")
        finally:
            self.stop_animation()
    
    def _build_scheduling_data(self, r): s={}; (s.update({"sS":str(r['Start Date'])}) if pd.notna(r.get('Start Date')) else None); (s.update({"sE":str(r['Due Date'])}) if pd.notna(r.get('Due Date')) else None); return {k:v for k,v in [("scheduledStart",s.get("sS")),("scheduledEnd",s.get("sE"))] if v} if s else None
    def _build_assignment_data(self, r): a={}; (a.update({"aT":r['Assigned To']}) if pd.notna(r.get('Assigned To')) else None); (a.update({"rev":r['Reviewer']}) if pd.notna(r.get('Reviewer')) else None); return {k:v for k,v in [("assignedTo",a.get("aT")),("reviewer",a.get("rev"))] if v} if a else None
    def _build_asset_data(self, r): assets={}; (assets.update({"iA":r['Link']}) if pd.notna(r.get('Link')) else None); return {"inputAsset":assets.get("iA")} if assets.get("iA") else None
    
    def run(self):
        self.log_message(f"🎬 {APP_TITLE} Ready!", clear_previous=True)
        self.log_message("📋 Select CSV, choose output, convert, then validate online.")
        if not TKSVG_AVAILABLE: self.log_message("ℹ️ For SVG logo, install 'tksvg': pip install tksvg")
        if 'requests' not in globals(): self.log_message("ℹ️ For online validation, install 'requests': pip install requests")
        self.log_message("")
        self.root.mainloop()

if __name__ == "__main__":
    print(f"🚀 Starting {APP_TITLE}...")
    print("✅ Validator-compliant | ✨ Online Validation Feature (/api/check)")
    app = ShotGridToOMCConverter()
    app.run()