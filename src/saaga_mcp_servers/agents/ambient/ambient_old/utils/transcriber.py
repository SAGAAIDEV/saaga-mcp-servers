import assemblyai as aai
from loguru import logger

# import pyaudio # Removed pyaudio
# import threading # Was unused
import sys
from ambient_old.config.settings import settings


class RealtimeTranscriber:
    """
    A class to handle real-time audio transcription using AssemblyAI,
    capturing audio from the microphone using AssemblyAI's MicrophoneStream.
    """

    def __init__(self, sample_rate=16000):  # Removed words_before_transcription
        """
        Initializes the RealtimeTranscriber.

        Args:
            sample_rate (int): The sample rate of the audio stream (e.g., 16000).
                               AssemblyAI recommends 16_000 for medium quality.
        """
        aai.settings.api_key = settings.ASSEMBLYAI_API_KEY
        print(f"AssemblyAI API key: {settings.ASSEMBLYAI_API_KEY[:5]}")
        self.sample_rate = sample_rate
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=self.sample_rate,
            word_boost=[
                "CURSOR_USER_QUERY_MARKER",
                "GEMINI_TOOL_CODE_MARKER",
                "GEMINI_CODE_OUTPUT_MARKER",
            ],  # Add any custom vocabulary
            on_data=self._on_data,
            on_error=self._on_error,
            on_open=self._on_open,
            on_close=self._on_close,
        )
        self.is_transcribing = False
        self.final_transcript = ""
        # self.microphone_stream is not stored as an instance variable,
        # as it's created and used locally within the start method per AssemblyAI example.

    def _on_data(self, transcript: aai.RealtimeTranscript):
        """Callback for when new transcription data is received."""
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            logger.info(f"Final Transcript: {transcript.text}")
            self.final_transcript += transcript.text + " "
            print(f"Final: {transcript.text}", end="\r\n")
        else:
            logger.info(f"Interim Transcript: {transcript.text}")
            print(f"Interim: {transcript.text}", end="\r")

    def _on_error(self, error: aai.RealtimeError):
        """Callback for when a transcription error occurs."""
        logger.error(f"Transcription error: {error}")
        self.is_transcribing = False  # Error likely means transcription stopped.

    def _on_open(self, session_opened: aai.RealtimeSessionOpened):
        """Callback for when the transcription session is opened."""
        logger.info(f"Transcription session opened: {session_opened.session_id}")

    def _on_close(self):
        """Callback for when the transcription session is closed by AssemblyAI."""
        logger.info("AssemblyAI transcription session closed (on_close callback).")
        self.is_transcribing = False  # Session is closed.

    def start(self):
        """Starts the real-time transcription process. This method is blocking."""
        if self.is_transcribing:
            logger.warning("Transcription is already in progress.")
            return

        logger.info("Starting real-time transcription...")
        self.is_transcribing = True
        self.final_transcript = ""

        try:
            self.transcriber.connect()  # Establish connection to AssemblyAI
            # session_id might not be available immediately after connect() if it's async,
            # but on_open callback will log it. For synchronous connect, it might be.
            # logger.info(f"Successfully connected to AssemblyAI. Session ID: {self.transcriber.session_id}")

            microphone_stream = aai.extras.MicrophoneStream(
                sample_rate=self.sample_rate
            )
            logger.info(
                "Microphone stream initiated. Streaming to AssemblyAI... Press Ctrl+C to stop."
            )

            # This call is blocking and will run until the stream is closed or interrupted.
            self.transcriber.stream(microphone_stream)

            self.transcriber.close()

        except KeyboardInterrupt:
            logger.info(
                "Keyboard interrupt received during transcription. Transcription will be stopped externally."
            )
            # Re-raise for the main handler in __main__ to call stop().
            raise
        except Exception as e:
            logger.error(f"Error during transcription start or streaming: {e}")
            # Re-raise for the main handler in __main__ to call stop().
            raise
        finally:
            # This block executes when stream() returns (normally or via an unhandled exception within it,
            # though KeyboardInterrupt is caught and re-raised above).
            logger.info(
                "Streaming has concluded or been interrupted in start() method."
            )
            self.is_transcribing = False  # Mark as no longer actively streaming.
            # The actual self.transcriber.close() is handled by the self.stop() method,
            # which should be called by the client (e.g., in a finally block in __main__).

    # Removed _audio_stream_callback as pyaudio is no longer used.
    # def _audio_stream_callback(self, in_data, frame_count, time_info, status):
    #    """Callback for the audio stream from PyAudio."""
    #    if self.is_transcribing and self.transcriber.status == aai.RealtimeTranscriberStatus.CONNECTED:
    #        self.transcriber.stream(in_data)
    #    return (in_data, pyaudio.paContinue)

    def stop(self):
        """
        Stops the real-time transcription process and closes the AssemblyAI connection.
        Returns the final accumulated transcript.
        """
        logger.info("Attempting to stop real-time transcription...")

        # Set is_transcribing to False as a primary action of stopping.
        self.is_transcribing = False

        # The MicrophoneStream from assemblyai.extras is managed by the RealtimeTranscriber.
        # When transcriber.close() is called, it should handle the underlying stream.

        try:
            if self.transcriber:
                logger.info(f"Closing AssemblyAI transcriber.")
                self.transcriber.close()
                # The on_close callback should also set self.is_transcribing to False.
                logger.info("AssemblyAI transcriber.close() called.")
            else:
                logger.info("AssemblyAI transcriber already closed or not initialized.")
        except Exception as e:
            logger.error(f"Error while closing AssemblyAI transcriber: {e}")

        logger.info(f"Final transcript: {self.final_transcript}")
        return self.final_transcript


def run_realtime_transcription():
    """Runs the real-time transcription process and returns the final transcript."""
    rt_transcriber = RealtimeTranscriber(sample_rate=16000)  # Standard sample rate
    final_text_result = ""
    try:
        # The start() method is now blocking and will run until Ctrl+C is pressed
        # or the stream naturally concludes (if applicable for MicrophoneStream).
        rt_transcriber.start()
    except KeyboardInterrupt:
        logger.info("User interrupted transcription via Ctrl+C in main function.")
    except Exception as e:
        logger.error(f"An unexpected error occurred in main function: {e}")
    finally:
        logger.info(
            "Ensuring transcription is stopped and resources are released via main function finally block..."
        )
        final_text_result = rt_transcriber.stop()
        logger.info(
            f'Transcription process officially stopped in main function. Final captured text: "{final_text_result.strip()}"'
        )
    return final_text_result


if __name__ == "__main__":
    # Example usage:
    final_transcript = run_realtime_transcription()
    logger.info(
        f'Final transcript returned by run_realtime_transcription: "{final_transcript.strip()}"'
    )
    logger.info(f"Exiting...\n")
    # sys.exit(0) # Removed to allow for more graceful shutdown
