/* In UTF-8 Lowercase n-with-tilde == ñ == U+00F1 == 0xC3 0xB1 == \303 \261 */
const char mañana tomorrow[] = "tomorrow"; /* valid UTF-8 but compilable */
// Undefined Behavior if built in UTF-8 locale