import tkinter as tk
from tkinter import messagebox

class StationMove(tk.Frame):
    def __init__(self, master, current_station="北千里", stations=None, ticket_fare=None, fares=None, switch_to_purchase=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.current_station = current_station
        self.selected_station = current_station
        self.stations = stations or []
        self.ticket_fare = ticket_fare  # 購入した切符の運賃
        self.fares = fares or {} # 駅間の運賃データ
        self.switch_to_purchase = switch_to_purchase

        if not self.stations:
            messagebox.showerror("エラー", "駅リストが指定されていません。")
            return

        if not self.fares:
            raise ValueError("運賃データが指定されていません。\n main.pyで正しく渡されているかを確認してください。")

        self.create_widgets()

    def create_widgets(self):
        # 現在地表示
        self.label_current_station = tk.Label(self, text=f"現在地: {self.selected_station}")
        self.label_current_station.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # 切符の運賃表示
        fare_text = f"{self.ticket_fare}円" if self.ticket_fare is not None else "運賃が設定されていません"
        self.label_ticket_fare = tk.Label(self, text=f"購入した切符の運賃: {fare_text}")
        self.label_ticket_fare.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # 駅移動ボタン
        self.button_prev_station = tk.Button(self, text="前の駅", command=self.move_to_prev_station)
        self.button_prev_station.grid(row=2, column=0, padx=10, pady=10)

        self.button_next_station = tk.Button(self, text="次の駅", command=self.move_to_next_station)
        self.button_next_station.grid(row=2, column=1, padx=10, pady=10)

        # 降車ボタン
        self.button_exit_station = tk.Button(self, text="降車", command=self.exit_station)
        self.button_exit_station.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def move_to_next_station(self):
        # 次の駅に移動する処理
        current_index = self.stations.index(self.selected_station)
        if current_index < len(self.stations) - 1:
            self.selected_station = self.stations[(current_index + 1) % len(self.stations)]
            self.label_current_station.config(text=f"現在地: {self.selected_station}")

    def move_to_prev_station(self):
        # 前の駅に移動する処理
        current_index = self.stations.index(self.selected_station)
        if current_index > 0:
            self.selected_station = self.stations[(current_index - 1) % len(self.stations)]
            self.label_current_station.config(text=f"現在地: {self.selected_station}")

    def exit_station(self):
        # 降車処理
        # 現在地と降車駅が同じ場合
        if self.selected_station == self.current_station:
            messagebox.showerror("エラー", "現在地と同じ駅では降車できません。")
            return

        # 運賃の取得
        fare = self.fares.get((self.current_station, self.selected_station), "運賃不明")
        if fare == "運賃不明":
            messagebox.showerror("エラー", "指定された駅間の運賃が不明です。")
            return

        # 切符の運賃以内で降車可能な場合
        if self.ticket_fare >= fare:
            messagebox.showinfo("降車", f"{self.selected_station}で降車しました。\nご利用ありがとうございました。")
            self.return_to_purchase()
        else:
            # 不足分を計算
            shortage = fare - self.ticket_fare
            self.request_additional_payment(shortage)

    def request_additional_payment(self, shortage):
        # 不足分の支払い画面を表示
        def confirm_payment():
            try:
                additional_payment = int(entry_payment.get())
                if additional_payment < shortage:
                    messagebox.showerror("エラー", f"不足分の{shortage - additional_payment}円が残っています。")
                else:
                    change = additional_payment - shortage
                    if change > 0:
                        messagebox.showinfo("支払い完了", f"追加支払いが完了しました。\nお釣りは{change}円です。\nご利用ありがとうございました。")
                    else:
                        messagebox.showinfo("支払い完了", "追加支払いが完了しました。\nご利用ありがとうございました。")
                
                    payment_window.destroy()
                    self.return_to_purchase()
            except ValueError:
                messagebox.showerror("エラー", "正しい金額を入力してください。")

        payment_window = tk.Toplevel(self)
        payment_window.title("追加支払い")
        tk.Label(payment_window, text=f"不足分: {shortage}円").grid(row=0, column=0, padx=10, pady=10)
        entry_payment = tk.Entry(payment_window)
        entry_payment.grid(row=1, column=0, padx=10, pady=10)
        tk.Button(payment_window, text="支払い", command=confirm_payment).grid(row=2, column=0, padx=10, pady=10)

    def return_to_purchase(self):
        # 切符購入画面に戻る処理
        self.current_station = self.selected_station
        self.switch_to_purchase(self.current_station)