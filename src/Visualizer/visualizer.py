import matplotlib.pyplot as plt
from src.Dto.vog_data_entity import VOGData


class VOGMatplotlibVisualizer:
    def plot(self, data: VOGData) -> None:
        fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
        df, t_col = data.df, data.time_col

        # Title Stamping
        title_str = f"[{data.group}] Session: {data.session_id} \n Task: {data.task_name} ({data.direction} Analysis)"
        fig.suptitle(title_str, fontsize=18, fontweight='bold')

        # View 1: Raw Signal
        axes[0].plot(df[t_col], df[data.target_col], label=f'Target', color='red', linestyle='--', linewidth=2)

        # [ARCHITECTURAL UPDATE] Render Anti-Saccade Expected Target
        if data.is_anti:
            axes[0].plot(df[t_col], df[data.expected_target_col], label='Expected Target (Anti)', color='magenta',
                         linestyle=':', linewidth=2)

        axes[0].plot(df[t_col], df[data.eye_col_l], label=f'Left Eye', color='blue', alpha=0.7)
        axes[0].plot(df[t_col], df[data.eye_col_r], label=f'Right Eye', color='green', alpha=0.7)
        axes[0].set_title('1. Raw Waveform: Target vs Eye Movement')
        axes[0].legend(loc='upper right')
        axes[0].grid(True, linestyle=':', alpha=0.6)

        # View 2: Tracking Error
        axes[1].axhline(0, color='red', linestyle='--', linewidth=1)
        axes[1].plot(df[t_col], df['Error_L'], label='Error (L - Expected)', color='purple', alpha=0.8)
        axes[1].plot(df[t_col], df['Error_R'], label='Error (R - Expected)', color='orange', alpha=0.8)
        axes[1].set_title('2. Derived Feature: Eye Tracking Error (Deviation from Expected)')
        axes[1].legend(loc='upper right')
        axes[1].grid(True, linestyle=':', alpha=0.6)

        # View 3: Cross-Axis Noise
        if data.noise_col_l and data.noise_col_r:
            axes[2].plot(df[t_col], df[data.noise_col_l], label='Left Noise', color='gray', alpha=0.7)
            axes[2].plot(df[t_col], df[data.noise_col_r], label='Right Noise', color='brown', alpha=0.7)
            axes[2].set_title('3. Outlier/Noise Monitoring (Orthogonal Cross-Axis)')
        else:
            axes[2].set_title('3. Outlier/Noise Monitoring (Data Not Available)')

        axes[2].set_xlabel('Time (sec)')
        axes[2].legend(loc='upper right')
        axes[2].grid(True, linestyle=':', alpha=0.6)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

        # OOM(Out of Memory) 방지를 위한 명시적 Garbage Collection
        plt.close(fig)