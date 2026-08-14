# Semgrep SAST

## Check installation

```cmd
semgrep --version
```

## Scan vulnerable source

```cmd
semgrep --config sast\semgrep-rules.yml src\vulnerable
```

## Save vulnerable findings

```cmd
semgrep --config sast\semgrep-rules.yml src\vulnerable --json > sast\semgrep-before.json
```

## Scan secure source

```cmd
semgrep --config sast\semgrep-rules.yml src\secure
```

## Save secure findings

```cmd
semgrep --config sast\semgrep-rules.yml src\secure --json > sast\semgrep-after.json
```

## Automatic Semgrep scan

You may also run:

```cmd
semgrep --config=auto src
```

Do not manually invent scan results. Put the actual Semgrep output in the
report/screenshots.
