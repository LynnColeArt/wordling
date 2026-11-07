# Bounded proofreading provider

`internal/proofreading` is the minimal resource/provider surface. It keeps
bounded dictionaries, suspect words and correction/ignore actions. It never
copies proprietary dictionary bytes and never claims original suggestion order
from a modern replacement.
