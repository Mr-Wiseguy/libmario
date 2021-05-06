DECOMP_INPUT_FILES := sm64/src/game/mario_actions_airborne.c sm64/src/game/mario_actions_automatic.c sm64/src/game/mario_actions_cutscene.c \
    sm64/src/game/mario_actions_moving.c sm64/src/game/mario_actions_object.c sm64/src/game/mario_actions_stationary.c sm64/src/game/mario_actions_submerged.c \
	sm64/src/game/mario_misc.c sm64/src/game/mario_step.c sm64/src/game/mario.c sm64/src/engine/math_util.c sm64/src/game/object_helpers.c

all: libmario.dll libmario.so

libmario.dll: $(wildcard mariolib/*.c) $(DECOMP_INPUT_FILES)
	x86_64-w64-mingw32-gcc $^ -o $@ -shared -DNON_MATCHING -DAVOID_UB -ggdb -Ism64/include -Ism64/src/engine -Ism64/src/game -Ism64/src -Ism64 -lm -Wl,--subsystem,windows

libmario.so: $(wildcard mariolib/*.c) $(DECOMP_INPUT_FILES)
	gcc $^ -o $@ -shared -DNON_MATCHING -DAVOID_UB -ggdb -Ism64/include -Ism64/src/engine -Ism64/src/game -Ism64/src -Ism64 -lm -fPIC
