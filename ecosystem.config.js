module.exports = {
    apps: [
        {
            namespace: "real-estate-develop-assistant-api",
            name: "main",
            watch: [
                "src",
            ],
            ignore_watch: [
                "**/__pycache__/**/*",
            ],
            // watch_delay: 2000,
            interpreter: "python",
            script: "main.py",
            args: "serve",
            instances: 1,
            exec_mode: "fork",
            env: {
                // "ENV": "development",
            },
        }
    ],
}