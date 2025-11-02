import type { ReactNode } from 'react';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { source } from '@/lib/source';
import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';

const baseOptions: BaseLayoutProps = {
  nav: {
    title: 'Python Binance',
  },
  links: [
    {
      text: 'GitHub',
      url: 'https://github.com/sammchardy/python-binance',
      active: 'nested-url',
    },
  ],
};

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <DocsLayout tree={source.pageTree} {...baseOptions}>
      {children}
    </DocsLayout>
  );
}
