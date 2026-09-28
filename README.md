# LiveWeb Samples

Three browser tasks and a login task on live websites, built by [HUD](https://hud.ai). Each task starts an agent on a real site and grades its answer against a rubric.

**Taskset:** https://www.hud.ai/tasksets/1fc0f549-5830-4061-bc3a-25ad502ce723/tasks

## Tasks

| Task | What the agent has to do | Grading |
| --- | --- | --- |
| `ladybird-spot-num` | Turn a 3D ladybird on Sketchfab and count the spots on its shell, head excluded | One integer. Each spot off costs 20 points, and a range or several totals scores 0. |
| `diamond-rose-seats` | Find the kitchen photos on diamondrosesanctuary.com and count the chairs at the table | Exact count |
| `epa-air-quality` | Use EPA's AirNow map to find air quality data near zip 35173 on April 19, 2024 | Site, site ID, pollutant, and daily AQI, weighted 20/20/30/30 |
| `costco-login` | Sign in to an existing Costco account, entering the email and password through a tool that keeps them out of tool output | Reaching sign-in, entering the credentials without exposing the password, a confirmed signed-in session, and an accurate report with no account changes, 25% each |

Answers and full rubrics are in [`tasks/samples.yaml`](tasks/samples.yaml).

`costco-login` runs on the `rfp-liveweb` environment and needs your own Costco account, saved in HUD as a credential profile named `costco`. Without one, it fails when you run with `--all`.

## Results

Six runs per model per task, September 2026. Scores are mean rubric rewards over runs that finished.

| Model | Ladybird | Chairs | AirNow |
| --- | ---: | ---: | ---: |
| GPT 6 Astra | 93.3% | 0% | 100% |
| Claude Fable 5.1 | 56.0% | 0% | 100% |
| Claude Sonnet 5 | 0% | 0% | 100% |
| Qwen 3.8 Max\* | 0% | 16.7% | 95.0% |

\* Qwen ran with shell and file tools but no computer-use tool. Its one Chairs success came from a run that [installed YOLO object detectors to count the chairs](https://www.hud.ai/shared/trace/5be58cf2-3472-41c2-970b-2c4acb0ac112).

## Run them

```bash
uv tool install hud --python 3.12 --force
hud set HUD_API_KEY=your-key   # from hud.ai settings
hud eval <taskset-name> claude --runtime hud --all --max-steps 300 -y
```

To copy these tasks into your own taskset:

```bash
hud sync tasks my-liveweb-samples tasks.py
```

`.hud_eval.toml` re-encodes screenshots as WebP, because full-size screenshots of the 3D viewer overrun the provider's request-size cap on long runs.

## License

[MIT](LICENSE)
