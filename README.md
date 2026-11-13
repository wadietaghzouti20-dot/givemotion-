# Givemotion Lab

Tablet-friendly project for creating RENDEVO motion-graphics videos with the official [Givemotion](https://github.com/givemotion/givemotion) engine.

## Cloud render (no local terminal needed)
1. Open the **Actions** tab.
2. Choose **Render Givemotion video**.
3. Tap **Run workflow**, keep `video.html`, and run.
4. Download the `givemotion-mp4` artifact from the completed run.

GitHub-hosted Actions runners install Node.js, Givemotion, Chrome and FFmpeg, then render the composition to MP4.

## Edit
Open `video.html` on GitHub, tap the pencil icon, edit the HTML/CSS, and commit. Run the workflow again.

## Important
Givemotion makes deterministic motion graphics from HTML/CSS/JS; it does not generate photorealistic footage or include an AI model. GitHub Actions has usage limits, so rendering is not unlimited. The project itself is MIT licensed.
