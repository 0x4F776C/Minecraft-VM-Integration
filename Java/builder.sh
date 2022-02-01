# Java builder

echo "[*] Building $1.java"

javac "$1.java"
sleep 1

echo "[~] Build complete"

java "$1"

echo "[~] End of builder script"