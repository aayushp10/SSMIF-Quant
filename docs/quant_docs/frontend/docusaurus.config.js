module.exports = {
  title: 'SSMIF Quant',
  tagline: 'For all of your quant related questions',
  url: 'https://your-docusaurus-test-site.com',
  baseUrl: '/docs/',
  onBrokenLinks: 'throw',
  favicon: 'img/q_logoT.png',
  organizationName: 'SSMIF-Quant', // Usually your GitHub org/user name.
  projectName: 'SSMIF Quant Documentation', // Usually your repo name.
  themeConfig: {
    navbar: {
      title: 'SSMIF Quant',
      logo: {
        alt: 'My Site Logo',
        src: 'img/q_logoT.png',
      },
      items: [
        {
          to: 'docs/',
          activeBasePath: 'docs',
          label: 'Docs',
          position: 'left',
        },
        {to: 'blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/facebook/docusaurus',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Factor Model',
              to: 'docs/',
            },
            {
              label: 'Risk Screen',
              to: 'docs/risk-screen',
            },
            {
              label: 'Bailey',
              to: 'docs/bailey',
            },
          ],
        },
        {
          title: 'Communication',
          items: [
            {
              label: 'Discord',
              href: 'https://discord.gg/gBNS4cd',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: 'blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/SSMIF-Quant/quant',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} SSMIF Documentation Built with Docusaurus.`,
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl:
            'https://github.com/SSMIF-Quant/quant/edit/main/docs/quant_docs/frontend/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/SSMIF-Quant/quant',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
