from src.half_duplex_orchestrator import HalfDuplexLoop

if __name__ == "__main__":
    print("--- Starting Phase 1: Voice Loop Active. Speak now. ---") # Add this line
    loop = HalfDuplexLoop(
        samplerate=16000,
        frame_ms=30,
        chunk_sec=2.0,
        silence_ms=500,
        energy_thresh=0.01
    )
    loop.run()
