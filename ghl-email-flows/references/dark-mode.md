# Dark-mode contract

## The failure this exists to prevent

Gmail on iOS and Android **partially inverts** an email's colours when the phone is in
dark mode. Partially is the problem. White text turns black, mid-tone colours wash out,
and dark or tinted backgrounds survive the inversion untouched. The result is black
text on a dark background: headlines and card copy simply vanish.

It passes every desktop preview. It fails on the phone, which is where most people read
email. This has been caught in live testing more than once, and it is the single most
common way a technically-correct email arrives unreadable.

**The rule that avoids it: white canvas, dark ink.** Do not design light text on a dark
background for email, however good it looks in the browser.

## Component recipe

| Component | Contract |
|---|---|
| Canvas | White background, dark ink text |
| Body cards | White background with a soft brand-coloured border |
| Tints | Reserve pale brand tints for small pills and labels only, never behind body copy |
| Copy bands | Readable copy sits on white, in ink or brand colour |
| Call to action | A solid brand-colour button with a white label. This is the one proven exception, and it survives inversion |
| Meaning | Never carry meaning in colour alone. If the colour inverts, the words must still say it |

Every new component inherits this model. A dark-mode failure blocks shipping. It is not
a polish item.

## Two-version output

The builder emits both versions from one source:

- A full document carrying `color-scheme: light dark` metadata
- A `prefers-color-scheme: dark` block
- A darkened outer shell
- A **white inner card**, preserving every ink-on-white pair inline

The dark version darkens the frame around the message, not the message. Inline styles
on the card are what survive Gmail's rewriting, so keep them inline rather than in a
stylesheet.

## Verification

1. Render the built HTML locally
2. Screenshot it with the browser forced to dark, then forced to light. With
   agent-browser: `agent-browser set media dark`, reload, screenshot, then the same
   with `light`
3. Inspect every text component that sits on a non-white background. Only the call to
   action should be left
4. Send an internal test and open it on a real phone in dark mode

Step 4 is stronger evidence than the first three combined, because it is the only one
running Gmail's actual renderer. Do it before every launch, not just the first one.

Release evidence is both screenshots, the API `previewUrl` viewed in dark mode, and
the phone test.
