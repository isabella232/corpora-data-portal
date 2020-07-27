// Initialize dotenv
require("dotenv").config({
  path: `.env.${process.env.NODE_ENV}`,
});

module.exports = {
  plugins: [
    "gatsby-plugin-typescript",
    "gatsby-plugin-react-helmet",
    "gatsby-plugin-root-import",
    "gatsby-plugin-styled-components",
    {
      options: {
        name: `images`,
        path: `${__dirname}/src/images`,
      },
      resolve: `gatsby-source-filesystem`,
    },
    `gatsby-plugin-theme-ui`,
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
    {
      options: {
        display: `minimal-ui`, // icon: `src/images/gatsby-icon.png`, // This path is relative to the root of the site.
        name: `gatsby-starter-default`,
        // eslint-disable-next-line @typescript-eslint/camelcase
        short_name: `starter`,
        // eslint-disable-next-line @typescript-eslint/camelcase
        start_url: `/`,
      },
      resolve: `gatsby-plugin-manifest`,
    },
  ],
  siteMetadata: {
    author: `@gatsbyjs`,
    description: `Kick off your next, great Gatsby project with this default starter. This barebones starter ships with the main Gatsby configuration files you might need.`,
    title: `data.humancellatlas.org`,
  },
};
