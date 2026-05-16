"""Audio recording component for Streamlit."""
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import sounddevice as sd
import soundfile as sf
import numpy as np
from io import BytesIO


class AudioRecorder:
    """Handles audio recording and playback."""
    
    def __init__(self, sample_rate: int = 16000, duration: int = 10):
        """
        Initialize audio recorder.
        
        Args:
            sample_rate: Sampling rate in Hz
            duration: Maximum recording duration in seconds
        """
        self.sample_rate = sample_rate
        self.duration = duration
    
    def record_audio(self) -> bytes:
        """
        Record audio from microphone using WebRTC.
        
        Returns:
            Audio data in bytes or None
        """
        try:
            # Configure WebRTC
            rtc_configuration = RTCConfiguration(
                {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            )
            
            webrtc_ctx = webrtc_streamer(
                key="audio-recorder",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=rtc_configuration,
                media_stream_constraints={"audio": True, "video": False},
                async_processing=True,
            )
            
            if webrtc_ctx.state.playing:
                st.info("🎙️ Recording in progress... Speak into your microphone")
            
            if webrtc_ctx.audio_processor:
                try:
                    audio_frames = webrtc_ctx.audio_processor.get_frames()
                    if audio_frames:
                        # Process audio frames
                        audio_data = self._process_audio_frames(audio_frames)
                        if audio_data:
                            st.success("✓ Recording captured")
                            return audio_data
                except Exception as e:
                    st.warning(f"Audio processing: {str(e)}")
            
            return None
        
        except Exception as e:
            st.warning(f"WebRTC error: {str(e)}. Using fallback recording method.")
            return self._fallback_record()
    
    @staticmethod
    def _process_audio_frames(audio_frames):
        """Process WebRTC audio frames into WAV bytes."""
        try:
            if not audio_frames:
                return None
            
            # Combine all frames
            audio_data = b"".join([frame.to_ndarray().tobytes() for frame in audio_frames])
            
            # Convert to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Convert to WAV bytes
            buffer = BytesIO()
            sf.write(buffer, audio_array, 16000, format='WAV')
            buffer.seek(0)
            
            return buffer.getvalue()
        except Exception as e:
            st.error(f"Frame processing error: {str(e)}")
            return None
    
    def _fallback_record(self) -> bytes:
        """Fallback recording method using sounddevice (no nested columns).
        
        Records audio with a simple UI using sounddevice and soundfile.
        """
        st.markdown("**Or record using your system microphone:**")
        
        if st.button("🎙️ Start Recording", key="start_record_fallback"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Record audio for the configured duration
                status_text.info("🔴 Recording in progress... speak now!")
                
                recording = sd.rec(
                    int(self.duration * self.sample_rate),
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype=np.int16
                )
                
                # Update progress
                for i in range(int(self.duration * 10)):
                    progress_bar.progress(min((i + 1) / (self.duration * 10), 1.0))
                    sd.wait(int(self.sample_rate / 10))
                
                # Convert to bytes
                buffer = BytesIO()
                sf.write(buffer, recording, self.sample_rate, format='WAV')
                buffer.seek(0)
                
                progress_bar.empty()
                status_text.success("✓ Recording complete!")
                
                return buffer.getvalue()
            
            except Exception as e:
                status_text.error(f"Recording failed: {str(e)}")
                progress_bar.empty()
                return None
        
        return None
    
    @staticmethod
    def play_audio(audio_data: bytes) -> None:
        """
        Play audio data.
        
        Args:
            audio_data: Audio data in bytes
        """
        if audio_data:
            st.audio(audio_data, format="audio/wav")
