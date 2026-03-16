# Yandex Metrika — Next.js Setup

## Using next/script (App Router)

```tsx
// components/yandex-metrika.tsx
'use client';

import Script from 'next/script';
import { useEffect } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';

declare global {
  interface Window {
    ym: (...args: unknown[]) => void;
  }
}

interface Props {
  counterId: number;
}

export function YandexMetrika({ counterId }: Props) {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  // Track SPA navigations
  useEffect(() => {
    if (typeof window.ym !== 'undefined') {
      const url = pathname + (searchParams?.toString() ? '?' + searchParams.toString() : '');
      window.ym(counterId, 'hit', url);
    }
  }, [pathname, searchParams, counterId]);

  return (
    <>
      {/* Load the Metrika tag.js library */}
      <Script
        src="https://mc.yandex.ru/metrika/tag.js"
        strategy="afterInteractive"
        onLoad={() => {
          window.ym(counterId, 'init', {
            clickmap: true,
            trackLinks: true,
            accurateTrackBounce: true,
            webvisor: true,
          });
        }}
      />
      <noscript>
        <div>
          <img
            src={`https://mc.yandex.ru/watch/${counterId}`}
            style={{ position: 'absolute', left: '-9999px' }}
            alt=""
          />
        </div>
      </noscript>
    </>
  );
}
```

**Important:** The `ym` global function is created by `tag.js`. Using `onLoad` ensures
`init` is called only after the script has loaded. The `(function(m,e,t,r,i,k,a){...})`
IIFE from the standard snippet is not needed here — `next/script` handles async loading.

## Usage in layout.tsx

```tsx
// app/layout.tsx
import { Suspense } from 'react';
import { YandexMetrika } from '@/components/yandex-metrika';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body>
        {children}
        <Suspense fallback={null}>
          <YandexMetrika counterId={Number(process.env.NEXT_PUBLIC_YM_COUNTER_ID)} />
        </Suspense>
      </body>
    </html>
  );
}
```

The `<Suspense>` wrapper is needed because `useSearchParams()` requires it in App Router.

## Environment variable

```env
# .env.local
NEXT_PUBLIC_YM_COUNTER_ID=12345678
```

## Tracking goals from components

```tsx
'use client';

export function ContactButton() {
  const handleClick = () => {
    if (typeof window.ym !== 'undefined') {
      window.ym(Number(process.env.NEXT_PUBLIC_YM_COUNTER_ID), 'reachGoal', 'contact_click');
    }
  };

  return <button onClick={handleClick}>Contact us</button>;
}
```

## Helper utility

```ts
// lib/metrika.ts
export function reachGoal(target: string, params?: Record<string, unknown>) {
  if (typeof window !== 'undefined' && typeof window.ym !== 'undefined') {
    const counterId = Number(process.env.NEXT_PUBLIC_YM_COUNTER_ID);
    if (params) {
      window.ym(counterId, 'reachGoal', target, params);
    } else {
      window.ym(counterId, 'reachGoal', target);
    }
  }
}

export function hitPage(url: string, options?: { title?: string; referer?: string }) {
  if (typeof window !== 'undefined' && typeof window.ym !== 'undefined') {
    const counterId = Number(process.env.NEXT_PUBLIC_YM_COUNTER_ID);
    window.ym(counterId, 'hit', url, options);
  }
}
```

## Static export considerations

For `output: 'export'` sites hosted on static storage (like Yandex Object Storage),
the counter works the same way. The tracking script loads from Yandex CDN and runs
client-side. No server-side setup needed.

**Important:** Do NOT use `ssr: true` in the init options for static exports — it
prevents the counter from initializing. Only use `ssr: true` with actual SSR (e.g.
Next.js with a Node.js server).
