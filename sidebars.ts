// ...existing code...
import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    'intro', // Keep existing intro
    {
      type: 'category',
      label: 'ROS 2 Fundamentals',
      link: { type: 'doc', id: 'ros2-fundamentals/index' }, // Link to the main chapter page
      items: [
        'ros2-fundamentals/what-is-ros2',
        'ros2-fundamentals/nodes',
        'ros2-fundamentals/topics',
        'ros2-fundamentals/services',
        'ros2-fundamentals/actions',
        'ros2-fundamentals/parameters',
        'ros2-fundamentals/launch-files',
        'ros2-fundamentals/messages-services',
        'ros2-fundamentals/debugging',
        'ros2-fundamentals/logging-lifecycle',
        'ros2-fundamentals/urdf',
        'ros2-fundamentals/visualization',
        'ros2-fundamentals/time',
        'ros2-fundamentals/architecture',
        'ros2-fundamentals/sensor-drivers',
        'ros2-fundamentals/motor-controllers',
        'ros2-fundamentals/capstone-preview',
        // Labs could be sub-categories or directly listed depending on desired depth
      ],
    },
    // Any other top-level items can go here
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
// ...existing code...