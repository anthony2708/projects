// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Services Portal",
  tagline: "The gateway of all services",
  url: "https://services.builetuananh.name.vn",
  baseUrl: "/",
  staticDirectories: ["public"],
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "facebook", // Usually your GitHub org/user name.
  projectName: "docusaurus", // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "vi",
    locales: ["vi"],
    localeConfigs: {
      vi: {
        htmlLang: "vi-VN",
      },
    },
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },

        docs: false,
        blog: false,
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        hideOnScroll: true,
        title: "Services Portal",
        logo: {
          alt: "Portal Logo",
          src: "img/ET_Logo.png",
        },
        items: [
          {
            type: "dropdown",
            label: "Dịch vụ",
            position: "left",
            items: [
              {
                label: "Youtube Downloader",
                to: "/youtube",
              },
              {
                label: "URL Shortener",
                to: "/url",
              },
              {
                label: "R&D Portal",
                href: "http://dev.builetuananh.name.vn",
              },
            ],
          },
          {
            href: "https://www.builetuananh.name.vn",
            label: "Cổng thông tin",
            position: "left",
          },
          {
            href: "https://github.com/anthony2708",
            "aria-label": "GitHub",
            className: "header-github-link",
            position: "right",
          },
          {
            type: "localeDropdown",
            position: "right",
          },
        ],
      },
      announcementBar: {
        id: "contact",
        content:
          "📧 <b>Email</b>: <a target='_blank' rel='noopener noreferrer' href='mailto:builetuananh2708@gmail.com'>builetuananh2708@gmail.com</a> | 📞 <b>Tel</b>: <a target='_blank' rel='noopener noreferrer' href='tel:+84937826135'>(+84/0) 937826135</a>",
        backgroundColor: "#a4e4dc",
        textColor: "#222",
        isCloseable: false,
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Dịch vụ",
            items: [
              {
                label: "Youtube Downloader",
                to: "/youtube",
              },
              {
                label: "URL Shortener",
                to: "/url",
              },
              {
                label: "R&D Portal",
                href: "http://dev.builetuananh.name.vn",
              },
            ],
          },
          {
            title: "Liên hệ",
            items: [
              {
                label: "GitHub",
                href: "https://github.com/anthony2708",
              },
              {
                label: "Cổng thông tin",
                href: "https://www.builetuananh.name.vn",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Anthony Bui Le Tuan Anh. Built with ❤️ & Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
