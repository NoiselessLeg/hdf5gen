<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/NoiselessLeg/hdf5gen">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">HDF5 Transform Generator</h3>

  <p align="center">
    This tool generates C++ shim code that will create custom compound HDF5 datatypes for classes,
    enums, unions, and structs. These datatypes can be used to write objects of these types to an HDF5
    file.
    <br />
    <a href="https://github.com/NoiselessLeg/hdf5gen"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The idea for this generator came about when I was given the task to convert many, many
pre-existing data types in a codebase to something that could be written to an HDF5 file.

Although the HDF5 object model is fairly well-designed, it is not a trivial task to manually
create hundreds of compound datatypes to model structures in pre-existing code. 

In addition, the documentation on appending to an HDF5 dataset is somewhat outdated (i.e., many sites referenced
in Q/A platforms have moved or no longer exist). This repository also contains a very simple HDF5 file
writer that can be used to create an HDF5 file, write all instances of a datatype to a designated dataset
for that type, and append to it. The library is organized that the generated code can be used in a "freestanding"
mode - i.e., you would not need the simple writer, and can effectively use the generated data types in your
own custom HDF5 file writing implementation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/NoiselessLeg/hdf5gen.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP 
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/NoiselessLeg/hdf5gen/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle)

Project Link: [https://github.com/NoiselessLeg/hdf5gen](https://github.com/NoiselessLeg/hdf5gen)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS 
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/NoiselessLeg/hdf5gen.svg?style=for-the-badge
[contributors-url]: https://github.com/NoiselessLeg/hdf5gen/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/NoiselessLeg/hdf5gen.svg?style=for-the-badge
[forks-url]: https://github.com/NoiselessLeg/hdf5gen/network/members
[issues-shield]: https://img.shields.io/github/issues/NoiselessLeg/hdf5gen.svg?style=for-the-badge
[issues-url]: https://github.com/NoiselessLeg/hdf5gen/issues
[license-shield]: https://img.shields.io/github/license/NoiselessLeg/hdf5gen.svg?style=for-the-badge
[license-url]: https://github.com/NoiselessLeg/hdf5gen/blob/main/LICENSE.txt
[product-screenshot]: images/screenshot.png
